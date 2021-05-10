from django.contrib import admin
from management.mixins import MixinAdmin
from exampleapp import forms, models


@admin.register(models.ExampleModel)
class ExampleAdmin(MixinAdmin):
    form = forms.ExampleForm
