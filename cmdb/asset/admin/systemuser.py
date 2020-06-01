from django.contrib import admin
from asset import forms, models
from reversion.admin import VersionAdmin


@admin.register(models.SystemUser)
class SystemUserAdmin(VersionAdmin):
    list_display = ('Name', 'Username', 'Protocol', 'Enabled', 'CreateDate')
    form = forms.SystemUserForm
    readonly_fields = ('CreateDate', 'LastPassword')
