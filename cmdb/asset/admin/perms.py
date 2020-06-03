from django.contrib import admin
from asset import forms, models
from reversion.admin import VersionAdmin


@admin.register(models.Permission)
class PermsAdmin(VersionAdmin):
    fields = ['Name', 'User', 'UserGroup', 'Asset', 'AssetGroup', 'SystemUser', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Enabled', 'CreateDate']
    form = forms.PermsForm
    list_per_page = 30
