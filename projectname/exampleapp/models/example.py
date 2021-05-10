from django.utils.translation import ugettext_lazy as _
from management.mixins import MixinUUIDModel, MixinQuerySet, UUIDManager


class ExampleQuerySet(MixinQuerySet):
    pass


class ExampleManager(UUIDManager):
    _queryset = ExampleQuerySet


class ExampleModel(MixinUUIDModel):
    objects = ExampleManager()

    def __str__(self):
        return self.Hostname + "-" + self.IP

    class Meta:
        verbose_name = _('Example')
        verbose_name_plural = _('Example')
