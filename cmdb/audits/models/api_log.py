from django.db import models
from django.utils.translation import ugettext_lazy as _
from user.models import User
from cmdb.mixin import MixinQuerySet, MixinManager, MixinModel


class ApiLogQuerySet(MixinQuerySet):
    pass


class ApiLogManager(MixinManager):
    _cache_all_bypass = True
    _queryset = ApiLogQuerySet


class ApiLog(MixinModel):
    Class = models.CharField(max_length=32, verbose_name=_('Class'))
    Function = models.CharField(max_length=32, verbose_name=_('Function'))
    User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    SourceIP = models.CharField(max_length=32, verbose_name=_('Source IP'))
    URI = models.CharField(max_length=1024, verbose_name=_('URI'))
    StatusCode = models.IntegerField(verbose_name=_('Status Code'), null=True)

    objects = ApiLogManager()
    _cache_all_bypass = True

    class Meta:
        verbose_name = _('ApiLog')
        verbose_name_plural = _('ApiLog')
        # permissions = [('view_self_assets', 'Can view self assets')]
