from django.contrib import admin
from certificate import forms, models
from utils.mixin import MixinAdmin


@admin.register(models.Certificate)
class CertificateAdmin(MixinAdmin):
    list_display = ('Name', 'Domain', 'Enabled', 'CreateDate')
    form = forms.CertificateForm
