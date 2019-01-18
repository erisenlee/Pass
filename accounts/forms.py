from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Your username','autofocus': True}))
    password = forms.CharField(label='Password', strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}), required=True)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')
        # field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }

  