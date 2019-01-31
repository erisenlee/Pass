from django import forms
from . import models

class AccountForm(forms.ModelForm):

    class Meta:
        model = models.Account
        fields = ('name', 'link', 'password', 'description')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'link':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
        }
        







