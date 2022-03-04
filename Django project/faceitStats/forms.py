from django import forms
from .models import Account

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['accountUrl']