from django.shortcuts import render, redirect
from .forms import FinancialDataForm
from .models import FinancialData

def user_dash_view(request):
    # Assuming FinancialDataForm is your form class for modifying FinancialData
    if request.method == 'POST':
        form = FinancialDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_dash')  # Redirect back to the user dashboard
    else:
        form = FinancialDataForm()  # Instantiate an empty form

    # You may also want to retrieve existing FinancialData object if it exists
    financial_data = FinancialData.objects.first()  # Or use appropriate logic to retrieve the existing data
    context = {'form': form, 'financial_data': financial_data}
    return render(request, 'your_app/user_dash.html', context)
