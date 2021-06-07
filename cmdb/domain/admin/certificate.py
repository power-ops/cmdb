from django.contrib import admin
from management.mixins import MixinAdmin
from domain import forms, models


@admin.register(models.Certificate)
class CertificateAdmin(MixinAdmin):
    list_display = ('Name', 'get_Domain', 'Status', 'ExpireDate')
    raw_id_fields = ('FDomain',)
    form = forms.CertificateForm
