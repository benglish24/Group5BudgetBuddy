from django import forms
from .models import FinancialData

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['salary', 'saving_percentage', 'fixed_percentage']
