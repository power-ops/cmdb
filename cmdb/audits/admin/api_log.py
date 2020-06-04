from django.contrib import admin
from reversion.admin import VersionAdmin

from audits import models


# Register your models here.
@admin.register(models.ApiLog)
class ApiLogAdmin(VersionAdmin):
    list_display = ('User', 'Function', 'Class', 'SourceIP', 'StatusCode', 'CreateDate')
    list_filter = ('User', 'Function', 'Class', 'SourceIP', 'StatusCode')
    search_fields = ('User', 'Function', 'Class', 'SourceIP')
    # form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    list_per_page = 30
    date_hierarchy = 'CreateDate'
    ordering = ('-id',)

    # fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled', 'CreateDate']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
