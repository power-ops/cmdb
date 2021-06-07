from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AssetConfig(AppConfig):
    name = 'asset'
    verbose_name = _('Asset')
