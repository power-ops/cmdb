from django import forms
from asset import models


class PermsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermsForm, self).__init__(*args, **kwargs)
        self.fields['User'].required = False
        self.fields['UserGroup'].required = False
        self.fields['Asset'].required = False
        self.fields['AssetGroup'].required = False

    class Meta:
        model = models.Permission
        fields = ['Name', 'User', 'UserGroup', 'Asset', 'AssetGroup', 'SystemUser', 'Enabled', 'CreateDate']
