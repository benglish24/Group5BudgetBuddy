from django.forms import ModelForm
from .models import UserDashboard, Transaction, Category
from django import forms

class UserDashboardForm(ModelForm):
    class Meta:
        model = UserDashboard
        fields = ['pay_amount', 'saving_percentage', 'spending']


class TransactionForm(ModelForm):
    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=categories)

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


class UploadReceiptForm(forms.Form):
    receipt_img = forms.ImageField(
        required=False,
    )

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CategoryReplacementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_category = kwargs.pop('current_category', None)
        super(CategoryReplacementForm, self).__init__(*args, **kwargs)
        self.fields['replacement_category'].queryset = Category.objects.exclude(id=current_category.id)

    replacement_category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Replacement Category')


class SalaryForm(ModelForm):
    class Meta:
        model = UserDashboard
        fields = ['pay_amount', 'saving_percentage', 'start_date', 'frequency']

        # makes date input in form an actual date picker
        widgets = {
            'start_date' : forms.widgets.DateInput(attrs={'type' : 'date'})
        }