from django import forms
from django.utils.translation import ugettext_lazy as _
from user import models
from django.contrib.auth import password_validation
from django.forms.widgets import PasswordInput, TextInput


class SuperUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': _('Username')}))
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    email = forms.EmailField(
        widget=TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': _('Email')}),
        required=False
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                          'autocomplete': 'new-password',
                                          'placeholder': _('Password')}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                          'autocomplete': 'new-password',
                                          'placeholder': _('Password Again')}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=True
    )

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.clean_password2())
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user
