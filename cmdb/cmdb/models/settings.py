from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinModel, MixinQuerySet, MixinManager
import jsonfield


class SettingsQuerySet(MixinQuerySet):
    pass


class SettingsManager(MixinManager):
    _queryset = SettingsQuerySet


class Settings(MixinModel):
    Name = models.CharField(max_length=128, verbose_name=_('Name'), unique=True)
    Configuration = jsonfield.JSONField(_('Configuration'), null=True)

    objects = SettingsManager()

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')
