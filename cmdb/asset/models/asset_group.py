from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinUUIDModel, MixinQuerySet, UUIDManager
from .asset import Asset


class AssetGroupQuerySet(MixinQuerySet):
    pass


class AssetGroupManager(UUIDManager):
    _queryset = AssetGroupQuerySet


class AssetGroup(MixinUUIDModel):
    Name = models.CharField(verbose_name=_('Name'), max_length=64, unique=True)
    Assets = models.ManyToManyField(Asset, verbose_name=_('Assets'))

    objects = AssetGroupManager()

    class Meta:
        verbose_name = _('Asset Group')
        verbose_name_plural = _('Asset Group')

    def __str__(self):
        return self.Name
