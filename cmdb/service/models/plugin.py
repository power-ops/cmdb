from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinModel, MixinQuerySet, MixinManager
import jsonfield


class PluginQuerySet(MixinQuerySet):
    pass


class PluginManager(MixinManager):
    _queryset = PluginQuerySet


class Plugin(MixinModel):
    Name = models.CharField(max_length=64, verbose_name=_("Name"))
    Version = models.CharField(max_length=16, verbose_name=_("Version"))
    InstallPackage = models.BinaryField(verbose_name=_("Install Package"))
    Configuration = jsonfield.JSONField(verbose_name=_('Configuration'), null=True)

    objects = PluginManager()

    class Meta:
        verbose_name = _('Plugin')
        verbose_name_plural = _('Plugin')
