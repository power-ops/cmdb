from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinUUIDModel, MixinQuerySet, UUIDManager
from .domain import Domain


class CertificateQuerySet(MixinQuerySet):
    pass


class CertificateManager(UUIDManager):
    _queryset = CertificateQuerySet


class Certificate(MixinUUIDModel):
    Name = models.CharField(max_length=128, verbose_name=_('Name'))
    Domain = models.ForeignKey(Domain, verbose_name=_('Domain'), on_delete=models.CASCADE)
    Password = models.CharField(max_length=128, verbose_name=_('Password'), null=True)
    Cert = models.BinaryField(_('Cert'), null=True, default=None)

    objects = CertificateManager()

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificate')
        # permissions = [('view_self_asset', 'Can view self assets')]
