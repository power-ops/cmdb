from django import forms
from management.utils import encrypt_ecb
from django.utils.translation import ugettext_lazy as _
from domain.models import Certificate, Domain
from django.contrib.admin import widgets
from django.contrib.admin.sites import site


class CertificateForm(forms.ModelForm):
    KeyFile = forms.FileField(label=_('KeyFile'), required=False)
    FDomain = forms.ModelChoiceField(queryset=Domain.objects.all(),
                                     label=_('Domain'),
                                     required=False,
                                     widget=widgets.ForeignKeyRawIdWidget(
                                         rel=Certificate._meta.get_field('FDomain').remote_field,
                                         admin_site=site
                                     ))
    Domain = forms.CharField(label=_('Domain'), required=False)
    Status = forms.CharField(label=_('Status'), required=False)
    Password = forms.CharField(label=_('Password'), required=False)
    ExpireDate = forms.DateTimeField(label=_("Expire Date"), required=False,
                                     widget=widgets.AdminSplitDateTime)

    def __init__(self, *args, **kwargs):
        super(CertificateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Certificate
        fields = ['Name', 'FDomain', 'Domain', 'Password', 'KeyFile', 'Status', 'ExpireDate', 'CreateDate']

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
