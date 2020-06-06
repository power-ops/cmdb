from django.contrib import admin
from worklink import models
from cmdb.mixin import MixinAdmin


@admin.register(models.WorkLink)
class WorkLinkAdmin(MixinAdmin):
    pass
