from django.db import models
from django.core.cache import cache
from django.http import Http404


class MixinManager(models.Manager):
    _cache_all_bypass = False

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


class UUIDManager(MixinManager):
    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()
