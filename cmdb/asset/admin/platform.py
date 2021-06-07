from django.contrib import admin
from asset import forms, models
from asset.mixin import MixinAdmin


@admin.register(models.Platform)
class PlatformAdmin(MixinAdmin):
    list_display = ('Name', 'Comment', 'Enabled', 'CreateDate')

