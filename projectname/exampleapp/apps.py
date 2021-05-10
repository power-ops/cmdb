from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class APPConfig(AppConfig):
    name = 'exampleapp'
    verbose_name = _('exampleapp')
