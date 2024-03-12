from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import UserDashboard, Transaction
from .decorators import authenticated_user
from .forms import TransactionForm, UploadForm

import csv

@authenticated_user
def user_dashboard(request):
    # Get or create the UserDashboard object for the current user
    # user_dashboard, created = UserDashboard.objects.get_or_create(custom_user=request.user)
    user_dashboard = UserDashboard.objects.get(custom_user=request.user)
    transactions = Transaction.objects.filter(user=request.user)

    # If the object was just created, it means it's empty and you might want to set default values here

    return render(request, 'user_dash.html', {'user_dashboard': user_dashboard, 'transactions' : transactions})


@authenticated_user
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('/')

    form = TransactionForm()
    context = {'form' : form, 'button_text' : 'Confirm'}
    return render(request, 'transaction_form.html', context)


@authenticated_user
def update_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    form = TransactionForm(instance=transaction)

    if request.user != transaction.user:
        return HttpResponse("You should not be here.")

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
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
            transactions = [] if 'file' not in request.FILES else csv.reader(decode_utf8(request.FILES['file']))
            next(transactions) # skip header

            for line in transactions:
                if not line[0]: continue

                date_of = line[0]
                amount = line[1]
                category = line[2]

                t = Transaction()
                t.date_of, t.amount, t.category = date_of, amount, category
                t.user = request.user
                t.save()

            return redirect('/')

    form = UploadForm()
    context = {"form" : form}
    return render(request, 'upload.html', context)