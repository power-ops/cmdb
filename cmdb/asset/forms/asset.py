from django import forms
from asset.models import Asset, Platform


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled']
