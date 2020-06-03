from django.contrib import admin
from reversion.admin import VersionAdmin
from dns import models


@admin.register(models.Record)
class RecordAdmin(VersionAdmin):
    list_display = (
        'Prefix', 'Domain', 'Type', 'Value', 'MxPriority', 'Circuit', 'Weight', 'TTL', 'LastUpdate', 'Enabled',
        'CreateDate')
    list_filter = ('Domain', 'Type', 'Circuit', 'TTL')
    search_fields = ('Prefix', 'Value')
    # form = forms.AssetForm
    readonly_fields = ('CreateDate', 'LastUpdate')
    fields = ['Prefix', 'Domain', 'Type', 'Value', 'MxPriority', 'Circuit', 'Weight', 'TTL', 'LastUpdate', 'Enabled',
              'CreateDate']
    list_per_page = 30
