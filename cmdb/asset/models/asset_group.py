from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel
from .asset import Asset


class AssetGroupQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class AssetGroupManager(models.Manager):
    pass


class AssetGroup(MixinModel):
    Name = models.CharField(verbose_name=_('Name'), max_length=64, unique=True)
    Assets = models.ManyToManyField(Asset, verbose_name=_('Assets'))

    objects = AssetGroupManager()

    def __str__(self):
        return self.Name
