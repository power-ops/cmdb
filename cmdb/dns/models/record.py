from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from cmdb.mixin import MixinUUIDModel, MixinQuerySet, UUIDManager
from .domain import Domain


class RecordQuerySet(MixinQuerySet):
    pass


class RecordManager(UUIDManager):
    pass


class Record(MixinUUIDModel):
    Domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    Prefix = models.CharField(max_length=128, verbose_name=_('Prefix'))
    Type = models.CharField(max_length=128, verbose_name=_('Type'))
    Value = models.CharField(max_length=128, verbose_name=_('Value'))
    MxPriority = models.IntegerField(verbose_name=_('MX Priority'), null=True)
    Circuit = models.CharField(max_length=128, verbose_name=_('Circuit'), null=True)
    Weight = models.IntegerField(verbose_name=_('Weight'), null=True)
    TTL = models.IntegerField(verbose_name=_('TTL'))
    LastUpdate = models.DateTimeField(_('Last Update'), default=timezone.now)

    objects = RecordManager()

    def __str__(self):
        return self.Prefix + '.' + self.Domain.Domain

    class Meta:
        verbose_name = _('Record')
        verbose_name_plural = _('Record')
        # permissions = [('view_self_assets', 'Can view self assets')]
