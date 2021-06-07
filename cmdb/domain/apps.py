from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DomainConfig(AppConfig):
    name = 'domain'
    verbose_name = _('Domain')
