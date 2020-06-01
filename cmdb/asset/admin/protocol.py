from django.contrib import admin
from asset import forms, models
from reversion.admin import VersionAdmin


@admin.register(models.Protocol)
class ProtocolAdmin(VersionAdmin):
    fields = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']

    # def has_add_permission(self, request):
    #     return True
