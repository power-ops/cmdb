from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import uuid
from django.core.cache import cache


class MixinModel(models.Model):
    Enabled = models.BooleanField(_('Enabled'), default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)
    _cache_all_bypass = False

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self._cache_all_bypass:
            cache.delete(self.__class__.__name__ + '.objects.all()')
        super(MixinModel, self).save(*args, **kwargs)


class MixinUUIDModel(MixinModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        abstract = True


class MixinQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class MixinManager(models.Manager):
    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()

    def get_queryset(self):
        return MixinQuerySet(self.model, using=self._db)

    def all(self):
        _class = str(self).split('.')[-2]
        if cache.get(_class + '.objects.all()'):
            return cache.get(_class + '.objects.all()')
        all = self.get_queryset().all()
        cache.set(_class + '.objects.all()', all)
        return all


class UUIDManager(MixinManager):
    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()
