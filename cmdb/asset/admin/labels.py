from django.contrib import admin


class LabelsAdmin(admin.ModelAdmin):
    fields = ['Name', 'Value', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Value', 'Enabled', 'CreateDate']

    def has_add_permission(self, request):
        return True
