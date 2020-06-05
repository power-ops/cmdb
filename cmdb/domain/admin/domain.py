from django.contrib import admin
from reversion.admin import VersionAdmin
from domain import models


@admin.register(models.Domain)
class DomainAdmin(VersionAdmin):
    list_display = ('Name', 'Domain', 'Status', 'ExpireDate', 'Enabled', 'CreateDate')
    list_filter = ('Status', 'Enabled')
    search_fields = ('Name', 'Domain')
    # form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    fields = ['Name', 'Domain', 'Status', 'ExpireDate', 'DnsServer', 'Enabled', 'CreateDate']
    list_per_page = 30
