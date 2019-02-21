from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.conf import settings
from captcha.fields import CaptchaField, CaptchaTextInput


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Your username', 'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Your password'}), required=True)
    if settings.CAPTCHA_ENABLE:
        captcha = CaptchaField(widget=CaptchaTextInput(
            attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'email': 'Please enter a valid email.',
        }
