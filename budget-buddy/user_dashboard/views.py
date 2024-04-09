from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages

from .models import UserDashboard, Transaction, Category
from .decorators import authenticated_user
from .forms import TransactionForm, UploadForm, CategoryForm, SalaryForm, CategoryReplacementForm
from collections import defaultdict

import csv
import json

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
            return redirect('/')

    form = TransactionForm(categories)

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
    context = {"form" : form}
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