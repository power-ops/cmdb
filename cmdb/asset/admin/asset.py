from django.contrib import admin
from asset import forms


# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    list_display = ('Hostname', 'IP', 'get_protocols', 'Enabled', 'CreateDate')
    list_filter = ('Labels',)
    form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled', 'CreateDate']
