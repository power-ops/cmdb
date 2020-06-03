from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CertificateConfig(AppConfig):
    name = 'certificate'
    verbose_name = _('Certificate')
