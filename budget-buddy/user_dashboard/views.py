from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse

from .models import UserDashboard, Transaction, Category
from .decorators import authenticated_user
from .forms import TransactionForm, UploadForm, CategoryForm, SalaryForm, CategoryReplacementForm, UploadReceiptForm

from collections import defaultdict

import csv
import json
import os

from pathlib import Path

from google.cloud import vision

from datetime import datetime
from dateutil import parser

@authenticated_user
def user_dashboard(request):
    dashboard = UserDashboard.objects.get(custom_user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    total_amount = dashboard.total_amount_for_user()

    # Filter transactions based on the start and end dates from the dashboard
    start_date = dashboard.start_date
    end_date = dashboard.end_date
    transactions_within_period = Transaction.objects.filter(user=request.user, date_of__range=[start_date, end_date])

    # Calculate expenses specifically for the doughnut chart within the given time period
    dct_chart = defaultdict(int)
    for t in transactions_within_period:
        dct_chart[t.get_category()] += t.get_amount()

    expenses_for_chart = json.dumps([
        {
            'category': category,
            'amount': dct_chart[category]
        }
        for category in dct_chart
    ])

    # Calculate total expenses for all transactions regardless of the time frame
    dct_all = defaultdict(int)
    for t in transactions:
        dct_all[t.get_category()] += t.get_amount()

    expenses = json.dumps([
        {
            'category': category,
            'amount': dct_all[category]
        }
        for category in dct_all
    ])

    context = {
        'dashboard': dashboard,
        'transactions': transactions,
        'categories': categories,
        'expenses': expenses,
        'expenses_for_chart': expenses_for_chart,
        'total_amount': total_amount,
    }

    return render(request, 'user_dash.html', context)


@authenticated_user
def add_transaction(request):
    # for passing into form's select field
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        form = TransactionForm(categories, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            dashboard = UserDashboard.objects.get(custom_user=request.user)
            dashboard.save()

            return redirect('/')

    print("REQUEST.GET")
    print(request.GET)


    date_string = "" if 'date' not in request.GET else request.GET['date']
    # date_of = "" if not date_string else datetime.strptime(date_string, '%m/%d/%Y').date()
    date_of = "" if not date_string else parser.parse(date_string)

    print(date_of)

    if date_of: date_of = datetime(date_of.year, date_of.month, date_of.day)

    amount = "" if 'amount' not in request.GET else request.GET['amount']

    category_name = "" if 'category' not in request.GET else request.GET['category']

    try:
        category = categories.get(name=category_name)
    except Category.DoesNotExist:
        category = None

    instance = Transaction(date_of=date_of, amount=amount, category=category)

    form = TransactionForm(categories, instance=instance)
    context = {'form' : form, 'button_text' : 'Confirm'}
    return render(request, 'transaction_form.html', context)


@authenticated_user
def update_transaction(request, pk):
    categories = Category.objects.filter(user=request.user)
    transaction = Transaction.objects.get(id=pk)

    form = TransactionForm(categories, instance=transaction)

    if request.user != transaction.user:
        return HttpResponse("You should not be here.")

    if request.method == 'POST':
        form = TransactionForm(categories, request.POST, instance=transaction)
        if form.is_valid():
            form.save()

            dashboard = UserDashboard.objects.get(custom_user=request.user)
            dashboard.save()

            return redirect('/')

    context = {'form' : form, 'button_text' : 'Confirm'}
    return render(request, 'transaction_form.html', context)


@authenticated_user
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)

    if request.user != transaction.user:
        return HttpResponse("You should not be here.")

    if request.method == 'POST':
        transaction.delete()
        return redirect('/')

    context = {"object" : transaction}
    return render(request, 'delete.html', context)


@authenticated_user
def upload_transaction(request):
    def decode_utf8(file):
        if not file: return
        for line in file:
            yield line.decode('utf-8')

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            categories = Category.objects.filter(user=request.user)
            category_list = [c.name for c in categories]
            transactions = [] if 'file' not in request.FILES else csv.reader(decode_utf8(request.FILES['file']))

            date_idx, amount_idx, category_idx = -1, -1, -1

            first_lines = [next(transactions), next(transactions)]
            print(first_lines)

            response = Gemini.get_csv_columns(first_lines)

            indices = json.loads(response.text)
            print(indices)

            date_idx, amount_idx, category_idx = indices['date'], indices['amount'], indices['category']

            # print(transactions)
            # next(transactions) # skip header



            for line in transactions:
                if not line[0]: continue

                date_of = line[date_idx]
                amount = line[amount_idx]
                category_name = line[category_idx].title()
                category = None

                if category_name in category_list:
                    category = categories.get(name=category_name)
                else:
                    category = Category(user=request.user, name=category_name)
                    category.save()
                    categories = Category.objects.filter(user=request.user)
                    category_list.append(category_name)

                t = Transaction()
                t.date_of, t.amount, t.category = date_of, amount, category
                t.user = request.user
                t.save()

            date_of = first_lines[1][date_idx]
            amount = first_lines[1][amount_idx]
            category_name = first_lines[1][category_idx].title()
            category = None

            if category_name in category_list:
                category = categories.get(name=category_name)
            else:
                category = Category(user=request.user, name=category_name)
                category.save()
                categories = Category.objects.filter(user=request.user)
                category_list.append(category_name)

            t = Transaction()
            t.date_of, t.amount, t.category = date_of, amount, category
            t.user = request.user
            t.save()

        dashboard = UserDashboard.objects.get(custom_user=request.user)
        dashboard.save()

        return redirect('/')

    form = UploadForm()
    upload_type = "Transactions File"

    context = {"form" : form, "upload_type" : upload_type}
    return render(request, 'upload.html', context)


@authenticated_user
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']

            # Check if a category with the same name already exists
            if Category.objects.filter(name=category_name, user=request.user).exists():
                # If it exists, display a warning message
                messages.warning(request, 'Category with this name already exists.')

                return redirect('add_category')  # Redirect back to the add category page

            # If the category doesn't exist, proceed to save it
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('/')

    form = CategoryForm()

    context = {'form': form, 'button_text': 'Confirm'}
    return render(request, 'category_form.html', context)


@authenticated_user
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    transactions_with_category = Transaction.objects.filter(category=category)

    if transactions_with_category.exists():
        if request.method == 'POST':
            form = CategoryReplacementForm(request.POST, current_category=category)
            if form.is_valid():
                replacement_category = form.cleaned_data['replacement_category']

                # Replace transactions with the selected replacement category
                Transaction.objects.filter(category=category).update(category=replacement_category)

                # Delete the category
                category.delete()

                return redirect('user_dash')
        else:
            form = CategoryReplacementForm(current_category=category)

        return render(request, 'cannot_delete_category.html', {'category': category, 'form': form, 'transactions': transactions_with_category})
    else:
        # No transactions associated with the category, delete it directly
        category.delete()
        return redirect('user_dash')


@authenticated_user
def delete_transactions(request, category_id):
    category = Category.objects.get(id=category_id)
    transactions_with_category = Transaction.objects.filter(category=category)

    if request.method == 'POST':
        # Delete transactions associated with the category
        transactions_with_category.delete()

        # Delete the category
        category.delete()

        return redirect('user_dash')

    return render(request, 'delete_transactions.html', {'category': category, 'transactions': transactions_with_category})


@authenticated_user
def update_information(request):
    dashboard = UserDashboard.objects.get(custom_user=request.user)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=dashboard)
        if form.is_valid():
            dashboard = form.save(commit=False)
            dashboard.salary = form.cleaned_data['salary']  # Update salary value
            dashboard.save()
            return redirect('/')
    else:
        form = SalaryForm(instance=dashboard)

    context = {'form': form, 'button_text': 'Update Information'}
    return render(request, 'update_information_form.html', context)



### AI STUFF


parent_dir = Path.cwd().parent
rel_path = 'detect-text-419721-92e36850ead7.json/'
src_path = (parent_dir / rel_path).resolve()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{src_path}"


class CloudVision(object):

    client = vision.ImageAnnotatorClient()

    @staticmethod
    def detect_text(img):

        content = img

        image = vision.Image(content=content)

        response = CloudVision.client.text_detection(image=image)
        texts = response.text_annotations

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        return texts



import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


class Gemini(object):

    model = genai.GenerativeModel('gemini-pro')

    @staticmethod
    def parse_receipt_data(receipt_data, category_names):
        response = Gemini.model.generate_content(f'''
                                        Here is some text from a receipt or invoice. Tell me the date of the transaction, the
                                        total amount of money involved in the transaction, and the category that this transaction
                                        best falls under given these categories: {category_names}.

                                        IMPORTANT: Output only in JSON format with keys named "date", "amount", and "category".
                                        Do NOT label the JSON as a json. The first character of the output should be a bracket denoting
                                        the beginning of the JSON string.

                                        For any of the three values you cannot find, output the value as a pair of empty quotes.
                                        Do NOT have any of the values be None. Do NOT have any of the values be an empty list.
                                        Date must be formatted in the form MM/DD/YYYY. You will choose exactly one category as a string if any
                                        are applicable. Output only the JSON string and nothing else.

                                        TEXT: {receipt_data}
                                            ''')
        return response

    @staticmethod
    def get_csv_columns(data):
        response = Gemini.model.generate_content(f'''
                                                    Here are the first two rows of a csv file, given as a list
                                                    where each item is a row in the csv file.

                                                    {data}

                                                    The file is meant to be a collection of a person's financial
                                                    transactions. Based on the data given, infer the column numbers,
                                                    starting from 0, that tell the date of a transaction, the amount of
                                                    money involved in a transaction, and the category of a transaction respectively.

                                                IMPORTANT: Output only in JSON format with keys named "date", "amount", and "category". The value
                                                    for each key should be the 0-indexed position of the data.
                                                Do NOT label the JSON as a json. The first character of the output should be a bracket denoting
                                                the beginning of the JSON string.

                                                For any of the three values you cannot find, output the value as the value -1.
                                                Do NOT have any of the values be None.
                                                    ''')

        return response

@authenticated_user
def upload_receipt(request):

    import base64
    import json


    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            categories = Category.objects.filter(user=request.user)
            category_names = [c.name for c in categories]

            img_obj = request.FILES['file']

            b64_img = base64.b64encode(img_obj.read())
            b64_string = str(b64_img, 'utf-8')

            texts = CloudVision.detect_text(b64_string)
            texts_as_string = ""

            for t in texts:
                texts_as_string += t.description + "\n"

            response = ""

            # print(texts_as_string)

            # tries the API call at most three times before giving up
            for _ in range(3):
                response = Gemini.parse_receipt_data(texts_as_string, category_names)
                if response.parts:
                    break

            if not response.parts: return redirect('add_transaction')

            print(response.text)

            dct = json.loads(response.text)
            print(dct)

            # date_string = "" if 'date' not in dct else dct['date']
            # amount = "" if 'amount' not in dct else dct['amount']
            # category_name = "" if 'category' not in dct else dct['category'].title()

            date_string = dct['date']
            amount = dct['amount']
            category_name = dct['category'].title()

            return redirect(reverse('add_transaction')+ f"?date={date_string}&amount={amount}&category={category_name}")

        return redirect('/')

    form = UploadReceiptForm()
    upload_type = "Receipt"

    context = {"form" : form, "upload_type" : upload_type}
    return render(request, 'upload_receipt.html', context)
