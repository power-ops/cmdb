from django import forms
from certificate.models import Certificate
from cmdb.utils import encrypt_ecb
from django.utils.translation import ugettext_lazy as _


class CertificateForm(forms.ModelForm):
    KeyFile = forms.FileField(label=_('KeyFile'), required=False)

    def __init__(self, *args, **kwargs):
        super(CertificateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Certificate
        fields = ['Name', 'Username', 'Password', 'KeyFile', 'Protocol', 'Enabled']

    def save(self, commit=True):
        instance = super(CertificateForm, self).save(commit=False)
        try:
            instance.Key = self.cleaned_data['KeyFile'].read()
        except:
            pass
        try:
            oj = Certificate.objects.get_by_id(instance.uuid)
            if (not oj) or (oj.Password != instance.Password):
                instance.Password = encrypt_ecb(instance.Password)
        except:
            pass
        return instance
