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
    # Get or create the UserDashboard object for    the current user

    # user_dashboard, created = UserDashboard.objects.get_or_create(custom_user=request.user)
    # If the object was just created, it means it's empty and you might want to set default values here
    dashboard = UserDashboard.objects.get(custom_user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    dct = defaultdict(int)

    # Calculate total transaction amount for current user
    total_amount = transactions.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    for t in transactions:
        dct[t.get_category()] += t.get_amount()

    expenses = json.dumps([
        {
        'category' : category,
        'amount' : dct[category]
        }
        for category in dct
    ])

    context = {'dashboard': dashboard,
               'transactions' : transactions,
               'categories' : categories,
               'expenses' : expenses,
               'total_amount' : total_amount,
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
            return redirect('/')

    print("REQUEST.GET")
    print(request.GET)


    date_string = "" if 'date' not in request.GET else request.GET['date']
    # date_of = "" if not date_string else datetime.strptime(date_string, '%m/%d/%Y').date()
    date_of = "" if not date_string else parser.parse(date_string)

    print(date_of)
    
    if date_of: 
        date_of = datetime(date_of.year, date_of.month, date_of.day)

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

            print(transactions)

            next(transactions) # skip header

            for line in transactions:
                if not line[0]: continue

                date_of = line[0]
                amount = line[1]
                category_name = line[2].title()
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


class GoogleCloud(object):

    client = vision.ImageAnnotatorClient()

    @staticmethod
    def detect_text(img):

        content = img

        image = vision.Image(content=content)

        response = GoogleCloud.client.text_detection(image=image)
        texts = response.text_annotations

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        return texts





import google.generativeai as genai
from dotenv import load_dotenv, dotenv_values

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


class GoogleGemini(object):
    
    model = genai.GenerativeModel('gemini-pro')

    @staticmethod
    def get_gemini_response(receipt_data, category_names):
        response = GoogleGemini.model.generate_content(f''' 
                                        Here is some text from a receipt or invoice. Tell me the date of the transaction, the
                                        total amount of money involved in the transaction, and the category that this transaction
                                        best falls under given these categories: {category_names}.

                                        IMPORTANT: Output only in JSON format with keys named "date", "amount", and "category". 
                                        Do NOT label the JSON as a json. The first character of the output should be a bracket denoting
                                        the beginning of the JSON string.

                                        For any of the three values you cannot find, output the value as a pair of empty quotes.
                                        Do NOT have any of the values be None. 
                                        Date must be formatted in the form MM/DD/YYYY. Output only the JSON string and nothing else.

                                        TEXT: {receipt_data}
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
            
            texts = GoogleCloud.detect_text(b64_string)
            texts_as_string = ""

            for t in texts:
                texts_as_string += t.description + "\n"
            
            response = ""

            # print(texts_as_string)

            # tries the API call at most three times before giving up
            for _ in range(3):
                response = GoogleGemini.get_gemini_response(texts_as_string, category_names)
                if response.parts: 
                    break
            
            if not response.parts: return redirect('add_transaction')

            dct = json.loads(response.text)

            date_string = "" if 'date' not in dct else dct['date']
            amount = "" if 'amount' not in dct else dct['amount']
            category_name = "" if 'category' not in dct else dct['category'].title()

            return redirect(reverse('add_transaction')+ f"?date={date_string}&amount={amount}&category={category_name}")

        return redirect('/')

    form = UploadReceiptForm()
    upload_type = "Receipt"

    context = {"form" : form, "upload_type" : upload_type}
    return render(request, 'upload_receipt.html', context)