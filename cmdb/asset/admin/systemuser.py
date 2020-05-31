from django.contrib import admin
from asset import forms


class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Username', 'Protocol', 'Enabled', 'CreateDate')
    form = forms.SystemUserForm
    readonly_fields = ('CreateDate', 'LastPassword')
