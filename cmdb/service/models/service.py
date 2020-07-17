from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinModel, MixinQuerySet, MixinManager
import jsonfield


class ServiceQuerySet(MixinQuerySet):
    pass


class ServiceManager(MixinManager):
    _queryset = ServiceQuerySet


class Service(MixinModel):
    Name = models.CharField(max_length=64, verbose_name=_("Name"))
    ServiceName = models.CharField(max_length=64, verbose_name=_("ServiceName"))
    Version = models.CharField(max_length=16, verbose_name=_("Version"))

    InstallScript = models.TextField(verbose_name=_("Install Script"), null=True)
    HealthCheckScript = models.TextField(verbose_name=_("Health Check Script"), null=True)
    AutoInstall = models.BooleanField(default=False, verbose_name=_("Auto Install"))

    objects = ServiceManager()

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Service')
