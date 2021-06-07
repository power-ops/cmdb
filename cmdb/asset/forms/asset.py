from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from asset import models


class AssetForm(forms.ModelForm):
    Protocols = forms.ModelMultipleChoiceField(
        queryset=models.Protocol.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Protocol'),
            is_stacked=False,
        )
    )
    Labels = forms.ModelMultipleChoiceField(
        queryset=models.Label.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Label'),
            is_stacked=False,
        )
    )

    class Meta:
        model = models.Asset
        fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled']
