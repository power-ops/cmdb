from django.db import models
from django.utils.translation import ugettext_lazy as _
from management.mixins import MixinUUIDModel, MixinQuerySet, UUIDManager
from .domain import Domain


class CertificateQuerySet(MixinQuerySet):
    pass


class CertificateManager(UUIDManager):
    _queryset = CertificateQuerySet


class Certificate(MixinUUIDModel):
    Name = models.CharField(max_length=128, verbose_name=_('Name'))

    FDomain = models.ForeignKey(Domain, verbose_name=_('Domain'), on_delete=models.CASCADE, null=True)
    Domain = models.CharField(max_length=128, verbose_name=_('Domain'), null=True)

    Status = models.CharField(max_length=128, verbose_name=_('Status'), null=True)
    ExpireDate = models.DateTimeField(_('Expire Date'), null=True)
    Password = models.CharField(max_length=128, verbose_name=_('Password'), null=True)
    Cert = models.BinaryField(_('Cert'), null=True, default=None)

    objects = CertificateManager()

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificate')
        # permissions = [('view_self_asset', 'Can view self assets')]

    def get_Domain(self):
        if self.FDomain:
            return self.FDomain.__str__()
        else:
            return self.Domain

    get_Domain.short_description = _('Domain')
