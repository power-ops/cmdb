from django.contrib import admin
from domain.admin import DomainAdmin as DA
from certificate import models


@admin.register(models.Domain)
class DomainAdmin(DA):
    pass
