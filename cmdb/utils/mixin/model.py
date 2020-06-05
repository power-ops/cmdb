from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.cache import cache
import uuid


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
