from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel, MixinQuerySet, UUIDManager
from .protocol import Protocol
from .platform import Platform
from .label import Label


class AssetQuerySet(MixinQuerySet):
    pass


class AssetManager(UUIDManager):
    def get_queryset(self):
        return AssetQuerySet(self.model, using=self._db)


class Asset(MixinModel):
    IP = models.CharField(max_length=128, verbose_name=_('IP'), db_index=True)
    Hostname = models.CharField(max_length=128, verbose_name=_('Hostname'))
    Protocols = models.ManyToManyField(Protocol, verbose_name=_('Protocol'))
    Platform = models.ForeignKey(Platform, default=Platform.default, on_delete=models.PROTECT,
                                 verbose_name=_("Platform"), related_name='assets')
    PublicIp = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Public IP'))
    Number = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('Asset number'))

    Labels = models.ManyToManyField(Label, blank=True, related_name='assets', verbose_name=_("Labels"))
    CreatedBy = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('Created by'))
    Comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))

    objects = AssetManager()

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Asset')
        permissions = [('view_self_assets', 'Can view self assets')]

    def get_protocols(self):
        return [p.__str__() for p in self.Protocols.all()]

    get_protocols.short_description = _('Protocols')

    def __str__(self):
        return self.Hostname + "-" + self.IP

    def has_label(self, label):
        L = str.split(label, ":")
        return self.Labels.filter(Name=L[0], Value=L[1])

    def set_label(self, label):
        L = str.split(label, ":")
        label, err = Label.objects.get_or_create(Name=L[0], Value=L[1])
        self.Labels.add(label.uuid)

    def json(self):
        return {
            "id": self.uuid,
            "ip": self.IP,
            "hostname": self.Hostname,
            "protocols": [p.json() for p in self.Protocols.all()]
        }
