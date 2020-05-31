from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import uuid


class MixinModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    Enabled = models.BooleanField(_('Enabled'), default=True)
    CreateDate = models.DateTimeField(_('Create Date'), default=timezone.now)

    def disable(self):
        self.Enabled = False
        self.save()

    def enable(self):
        self.Enabled = True
        self.save()

    class Meta:
        abstract = True
