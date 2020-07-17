from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import ugettext_lazy as _


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': _('Username')}))
    password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': _('Password')}))
