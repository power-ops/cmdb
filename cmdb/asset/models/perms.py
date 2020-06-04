from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from asset.models import Asset, SystemUser, AssetGroup
from utils.mixin import MixinModel, UUIDManager, MixinQuerySet


class PermissionQuerySet(MixinQuerySet):
    pass


class PermissionManager(UUIDManager):
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
        verbose_name = _('Permission')
        verbose_name_plural = _('Permission')
