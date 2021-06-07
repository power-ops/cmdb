from django.db import models
from user.models import User, Group
from django.utils.translation import ugettext_lazy as _
from asset.models import Asset, SystemUser, AssetGroup
from management.mixins import MixinUUIDModel, UUIDManager, MixinQuerySet
from django.core.cache import cache
from django.db.models import Q


class PermissionQuerySet(MixinQuerySet):
    pass


class PermissionManager(UUIDManager):
    _queryset = PermissionQuerySet

    def UserAssets(self, User):
        """
        :param User: UserObject
        :return: object: {
            AssetObject: [SystemUserObject]
        }
        """

        if cache.get('PermissionUserAssets.' + User.id):
            return cache.get('PermissionUserAssets.' + User.id)
        assets = {}
        for res in self._queryset.filter(
                Q(UserGroup__in=[g.id for g in User.groups.all()]) | Q(User=User.id)):
            system_user = [su for su in res.SystemUser.filter(Enabled=True).all()]
            for asset in res.Asset.filter(Enabled=True).all():
                if asset not in assets:
                    assets[asset] = system_user
                else:
                    assets[asset].extend(system_user)
            for assetGroup in res.AssetGroup.all():
                for asset in assetGroup.Assets.all():
                    if asset not in assets:
                        assets[asset] = system_user
                    else:
                        assets[asset].extend(system_user)
        for asset, system_user in assets.items():
            assets[asset] = list(set(system_user))
        cache.set('PermissionUserAssets.' + User.id, assets)
        return assets


class Permission(MixinUUIDModel):
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
        verbose_name = _('Asset Permission')
        verbose_name_plural = _('Asset Permission')
