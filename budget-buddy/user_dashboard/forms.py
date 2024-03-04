from django import forms
from .models import UserDashboard

class UserDashboardForm(forms.ModelForm):
    class Meta:
        model = UserDashboard
        fields = ['salary', 'saving_percentage', 'fixed_percentage', 'spending']
