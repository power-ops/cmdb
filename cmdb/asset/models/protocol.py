from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel


class ProtocolQuerySet(models.QuerySet):
    pass


class ProtocolManager(models.Manager):
    def get_queryset(self):
        return ProtocolQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).first()


class Protocol(MixinModel):
    Name = models.CharField(_('Name'), max_length=64, unique=True)
    Protocol = models.CharField(_('Protocol'), max_length=64)
    Port = models.IntegerField(_('Port'))

    objects = ProtocolManager()

    def __str__(self):
        return self.Name + '/' + str(self.Port)

    class Meta:
        verbose_name = _('Protocol')
        verbose_name_plural = _('Protocol')

    def json(self):
        return {
            "name": self.Name,
            "protocol": self.Protocol,
            "port": self.Port
        }
