from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ManagementConfig(AppConfig):
    name = 'Management'
    verbose_name = _('Management')
