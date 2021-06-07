from django.contrib import admin
from asset import forms, models
from management.mixins import MixinAdmin


@admin.register(models.Permission)
class PermsAdmin(MixinAdmin):
    fields = ['Name', 'User', 'UserGroup', 'Asset', 'AssetGroup', 'SystemUser', 'Enabled', 'CreateDate']
    list_display = ['Name', 'Enabled', 'CreateDate']
    form = forms.PermsForm
