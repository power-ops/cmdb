from django import forms
from asset import models
from user.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple


class PermsForm(forms.ModelForm):
    User = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('User'),
            is_stacked=False,
        )
    )
    UserGroup = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('User Group'),
            is_stacked=False,
        )
    )
    Asset = forms.ModelMultipleChoiceField(
        queryset=models.Asset.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Asset'),
            is_stacked=False,
        )
    )
    AssetGroup = forms.ModelMultipleChoiceField(
        queryset=models.AssetGroup.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Asset'),
            is_stacked=False,
        )
    )
    SystemUser = forms.ModelMultipleChoiceField(
        queryset=models.SystemUser.objects.all(),
        required=True,
        widget=FilteredSelectMultiple(
            verbose_name=_('System User'),
            is_stacked=False,
        )
    )

    class Meta:
        model = models.Permission
        fields = ['Name', 'User', 'UserGroup', 'Asset', 'AssetGroup',
                  'SystemUser', 'Enabled', 'CreateDate']
