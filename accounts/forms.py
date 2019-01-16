from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
