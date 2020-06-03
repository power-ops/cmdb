from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from utils.mixin import MixinModel
from .domain import Domain


class RecordQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class RecordManager(models.Manager):
    def get_queryset(self):
        return RecordQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()


class Record(MixinModel):
    Domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    Prefix = models.CharField(max_length=128, verbose_name=_('Prefix'))
    Type = models.CharField(max_length=128, verbose_name=_('Type'))
    Value = models.CharField(max_length=128, verbose_name=_('Value'))
    MxPriority = models.IntegerField(verbose_name=_('MX Priority'))
    Circuit = models.CharField(max_length=128, verbose_name=_('Circuit'))
    Weight = models.IntegerField(verbose_name=_('Weight'))
    TTL = models.IntegerField(verbose_name=_('TTL'))
    LastUpdate = models.DateTimeField(_('Last Update'), default=timezone.now)

    objects = RecordManager()

    class Meta:
        verbose_name = _('Record')
        verbose_name_plural = _('Record')
        # permissions = [('view_self_assets', 'Can view self assets')]
