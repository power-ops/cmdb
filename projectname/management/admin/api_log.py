from django.contrib import admin
from management.mixins import MixinAdmin
from management import models


@admin.register(models.ApiLog)
class ApiLogAdmin(MixinAdmin):
    list_display = ('User', 'Function', 'Class', 'SourceIP', 'StatusCode', 'CreateDate')
    list_filter = ('User', 'Function', 'Class', 'SourceIP', 'StatusCode')
    search_fields = ('User', 'Function', 'Class', 'SourceIP')
    # form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    ordering = ('-id',)

    # fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled', 'CreateDate']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
