from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Your username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}), required=True)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Your username'}))
    email = forms.EmailField(label='Email',required=True,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Your email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}), required=True)
    password2 = forms.CharField(label='Conform Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password again'}), required=True)
    