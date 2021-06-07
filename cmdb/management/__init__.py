from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ManagementConfig(AppConfig):
    name = 'management'
    verbose_name = _('Management')


default_app_config = 'management.ManagementConfig'
