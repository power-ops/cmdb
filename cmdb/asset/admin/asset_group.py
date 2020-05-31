from django.contrib import admin
from asset import forms


# Register your models here.
class AssteGroupAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Enabled', 'CreateDate')
    form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    fields = ['Name', 'Assets', 'Enabled', 'CreateDate']
