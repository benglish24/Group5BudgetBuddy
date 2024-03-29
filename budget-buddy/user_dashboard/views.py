from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import UserDashboard, Transaction, Category
from .decorators import authenticated_user
from .forms import TransactionForm, UploadForm, CategoryForm, SalaryForm

from collections import defaultdict

import csv
import json

@authenticated_user
def user_dashboard(request):
    # Get or create the UserDashboard object for the current user

    # user_dashboard, created = UserDashboard.objects.get_or_create(custom_user=request.user)
    # If the object was just created, it means it's empty and you might want to set default values here

    dashboard = UserDashboard.objects.get(custom_user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    dct = defaultdict(int)

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
               'expenses' : expenses}

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


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('/')

    form = CategoryForm()
    context = {'form' : form, 'button_text' : 'Confirm'}
    return render(request, 'category_form.html', context)

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

