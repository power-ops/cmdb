from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from asset.models import Asset, SystemUser, AssetGroup
from utils.mixin import MixinModel


class PermissionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class PermissionManager(models.Manager):
    pass


class Permission(MixinModel):
    Name = models.CharField(verbose_name=_('Name'), max_length=64)
    User = models.ManyToManyField(User, default=None)
    UserGroup = models.ManyToManyField(Group, default=None)
    Asset = models.ManyToManyField(Asset, default=None)
    AssetGroup = models.ManyToManyField(AssetGroup, default=None)
    SystemUser = models.ManyToManyField(SystemUser)

    objects = PermissionManager()

    def __str__(self):
        return self.Name

    class Meta:
        # db_table = 'Permission'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permission')
