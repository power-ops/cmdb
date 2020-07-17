from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinUUIDModel, MixinQuerySet, UUIDManager


class DomainQuerySet(MixinQuerySet):
    pass


class DomainManager(UUIDManager):
    _queryset = DomainQuerySet


class Domain(MixinUUIDModel):
    Name = models.CharField(max_length=128, verbose_name=_('Name'))
    SubDomain = models.CharField(max_length=128, verbose_name=_('Domain'), null=True, default='')
    Domain = models.CharField(max_length=128, verbose_name=_('Domain'))
    Status = models.CharField(max_length=128, verbose_name=_('Status'), null=True)
    ExpireDate = models.DateTimeField(_('Expire Date'), null=True)

    DnsServer = models.TextField(verbose_name=_('DNS Server'), null=True)

    objects = DomainManager()

    def __str__(self):
        if self.SubDomain:
            return self.SubDomain + '.' + self.Domain
        else:
            return self.Domain

    class Meta:
        verbose_name = _('Domain')
        verbose_name_plural = _('Domain')
        # permissions = [('view_self_assets', 'Can view self assets')]
