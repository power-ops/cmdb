from django.contrib import admin
from asset import forms, models
from reversion.admin import VersionAdmin


@admin.register(models.AssetGroup)
class AssteGroupAdmin(VersionAdmin):
    list_display = ('Name', 'Enabled', 'CreateDate')
    form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    fields = ['Name', 'Assets', 'Enabled', 'CreateDate']
