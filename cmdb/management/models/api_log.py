from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.http import Http404
from django.utils import timezone
try:
    from user.models import User
except:
    from django.contrib.auth.models import User


class ApiLogQuerySet(models.QuerySet):
    pass


class ApiLogManager(models.Manager):
    _cache_all_bypass = True
    _queryset = ApiLogQuerySet

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def get_queryset(self):
        if self._queryset:
            return self._queryset(self.model, using=self._db)
        else:
            raise Http404

    def all(self):
        if self._cache_all_bypass:
            return self.get_queryset().all()
        _class = str(self).split('.')[-2]
        if cache.get(_class + '.objects.all()'):
            return cache.get(_class + '.objects.all()')
        all = self.get_queryset().all()
        cache.set(_class + '.objects.all()', all)
        return all


class ApiLog(models.Model):
    Class = models.CharField(max_length=32, verbose_name=_('Class'))
    Function = models.CharField(max_length=32, verbose_name=_('Function'))
    User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    SourceIP = models.CharField(max_length=32, verbose_name=_('Source IP'))
    URI = models.CharField(max_length=1024, verbose_name=_('URI'))
    StatusCode = models.IntegerField(verbose_name=_('Status Code'), null=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    objects = ApiLogManager()
    _cache_all_bypass = True

    class Meta:
        verbose_name = _('ApiLog')
        verbose_name_plural = _('ApiLog')
        # permissions = [('view_self_assets', 'Can view self assets')]

    def save(self, *args, **kwargs):
        if not self._cache_all_bypass:
            cache.delete(self.__class__.__name__ + '.objects.all()')
        super(ApiLog, self).save(*args, **kwargs)
