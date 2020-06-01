from django.contrib import admin
from asset import models
from reversion.admin import VersionAdmin


@admin.register(models.Label)
class LabelsAdmin(VersionAdmin):
    fields = ['Name', 'Value', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Value', 'Enabled', 'CreateDate']

    # def has_add_permission(self, request):
    #     return True
