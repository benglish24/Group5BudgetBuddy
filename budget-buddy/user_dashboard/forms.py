from django.forms import ModelForm
from .models import UserDashboard, Transaction
from django import forms

class UserDashboardForm(ModelForm):
    class Meta:
        model = UserDashboard
        fields = ['salary', 'saving_percentage', 'fixed_percentage', 'spending']

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['date_of', 'amount', 'category']

        # makes date input in form an actual date picker
        widgets = {
            'date_of' : forms.widgets.DateInput(attrs={'type' : 'date'})
        }

class UploadForm(forms.Form):
    csv_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class' : 'form-control',
                                      'placeholder' : 'Upload your file',
                                      'help_text' : 'Select a .csv file to upload.'}))