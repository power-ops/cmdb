from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinUUIDModel, MixinQuerySet, UUIDManager


class WorkLinkQuerySet(MixinQuerySet):
    pass


class WorkLinkManager(UUIDManager):
    _queryset = WorkLinkQuerySet


class WorkLink(MixinUUIDModel):
    objects = WorkLinkManager()

    class Meta:
        verbose_name = _('Work Link')
        verbose_name_plural = _('Work Link')
        # permissions = [('view_self_asset', 'Can view self assets')]
