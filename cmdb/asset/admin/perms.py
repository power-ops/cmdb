from django.contrib import admin
from asset import forms


class PermsAdmin(admin.ModelAdmin):
    fields = ['Name', 'User', 'UserGroup', 'Asset', 'AssetGroup', 'SystemUser', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Enabled', 'CreateDate']
    form = forms.PermsForm
