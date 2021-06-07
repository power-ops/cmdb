from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from asset import models


class AssetGroupForm(forms.ModelForm):
    Assets = forms.ModelMultipleChoiceField(
        queryset=models.Asset.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Asset'),
            is_stacked=False,
        )
    )

    class Meta:
        model = models.Permission
        fields = ['Name', 'Assets', 'Enabled', 'CreateDate']
