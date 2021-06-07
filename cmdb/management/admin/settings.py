from django.contrib import admin
from management.mixins import MixinAdmin
from management import models


@admin.register(models.Settings)
class SettingsAdmin(MixinAdmin):
    list_display = ('Name', 'CreateDate')
    list_filter = ('Name',)
    search_fields = ('Name',)
    readonly_fields = ('CreateDate',)
    ordering = ('-id',)
