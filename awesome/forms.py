from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Fieldset, Submit
from django.urls import reverse

class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Create new account',
                'name',
                'link',
                'password',
                'description'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                
            )
        )
        # self.helper.form_action = reverse('awesome:account_create')
        # self.helper.add_input(Submit('submit', 'Submit'))
        # self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.Account
        fields = ('name', 'link', 'password', 'description')
       







