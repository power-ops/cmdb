from django.contrib import admin
from asset import forms


class ProtocolAdmin(admin.ModelAdmin):
    fields = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']

    def has_add_permission(self, request):
        return True
