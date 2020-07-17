from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission
from user import models
from django.contrib.auth import password_validation


class UserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('User Group'),
            is_stacked=False,
        ),
        label=_('User Group')
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Permission'),
            is_stacked=False,
        ),
        label=_('Permission')
    )
    avatar = forms.ImageField(required=False, label=_('Avatar'))

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'avatar', 'is_staff', 'is_active',
                  'date_joined', 'last_login', 'is_superuser', 'groups', 'user_permissions']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('User Group'),
            is_stacked=False,
        ),
        label=_('User Group')
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Permission'),
            is_stacked=False,
        ),
        label=_('Permission')
    )
    avatar = forms.ImageField(required=False, label=_('Avatar'))

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar', 'is_staff',
                  'is_active',
                  'date_joined', 'last_login', 'is_superuser', 'groups', 'user_permissions']

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
        if commit:
            user.save()
        return user
