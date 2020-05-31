from django import forms
from asset.models import SystemUser, Protocol
from utils.password import encrypt_ecb
from django.utils.translation import ugettext_lazy as _


class SystemUserForm(forms.ModelForm):
    Protocol = forms.CharField(widget=forms.Select())
    Password = forms.CharField(required=False)
    KeyFile = forms.FileField(label=_('KeyFile'), required=False)

    def __init__(self, *args, **kwargs):
        super(SystemUserForm, self).__init__(*args, **kwargs)
        self.fields['Protocol'].widget.choices = Protocol.objects.values_list('Protocol', 'Protocol').distinct()

    class Meta:
        model = SystemUser
        fields = ['Name', 'Username', 'Password', 'KeyFile', 'Protocol', 'Enabled']

    def save(self, commit=True):
        instance = super(SystemUserForm, self).save(commit=False)
        try:
            instance.Key = self.cleaned_data['KeyFile'].read()
        except:
            pass
        try:
            oj = SystemUser.objects.get_by_id(instance.uuid)
            if (not oj) or (oj.Password != instance.Password):
                instance.Password = encrypt_ecb(instance.Password)
        except:
            pass
        return instance
