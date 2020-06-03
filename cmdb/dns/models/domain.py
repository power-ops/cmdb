from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel


class DomainQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class DomainManager(models.Manager):
    def get_queryset(self):
        return DomainQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()


class Domain(MixinModel):
    Name = models.CharField(max_length=128, verbose_name=_('Name'))
    Domain = models.CharField(max_length=128, verbose_name=_('Domain'))
    Status = models.CharField(max_length=128, verbose_name=_('Status'))
    DnsServer = models.TextField(verbose_name=_('DNS Server'))
    ExpireDate = models.DateTimeField(_('Expire Date'), null=True)
    objects = DomainManager()

    class Meta:
        verbose_name = _('Domain')
        verbose_name_plural = _('Domain')
        # permissions = [('view_self_assets', 'Can view self assets')]
