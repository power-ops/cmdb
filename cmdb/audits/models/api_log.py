from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User


class ApiLogQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class ApiLogManager(models.Manager):
    def get_queryset(self):
        return ApiLogQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()


class ApiLog(models.Model):
    Class = models.CharField(max_length=32, verbose_name=_('Class'))
    Function = models.CharField(max_length=32, verbose_name=_('Function'))
    User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    SourceIP = models.CharField(max_length=32, verbose_name=_('Source IP'))
    URI = models.CharField(max_length=1024, verbose_name=_('URI'))
    StatusCode = models.IntegerField(verbose_name=_('Status Code'), null=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = ApiLogManager()

    class Meta:
        verbose_name = _('ApiLog')
        verbose_name_plural = _('ApiLog')
        # permissions = [('view_self_assets', 'Can view self assets')]
    #
    # def __str__(self):
    #     return self.Hostname + "-" + self.IP
