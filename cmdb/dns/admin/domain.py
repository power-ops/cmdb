from django.contrib import admin
from domain.admin import DomainAdmin as DA
from dns import models


@admin.register(models.Domain)
class DomainAdmin(DA):
    pass
