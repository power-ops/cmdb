from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinUUIDModel, MixinQuerySet, UUIDManager


class WorkLinkQuerySet(MixinQuerySet):
    pass


class WorkLinkManager(UUIDManager):
    _queryset = WorkLinkQuerySet


class WorkLink(MixinUUIDModel):
    Name = models.CharField(max_length=128, verbose_name=_("Name"))
    Link = models.CharField(max_length=1024, verbose_name=_("Link"))

    objects = WorkLinkManager()

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = _('Work Link')
        verbose_name_plural = _('Work Link')
        # permissions = [('view_self_asset', 'Can view self assets')]
