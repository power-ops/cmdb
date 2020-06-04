from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel, MixinQuerySet, UUIDManager


class LabelQuerySet(MixinQuerySet):
    pass


class LabelManager(UUIDManager):
    pass


class Label(MixinModel):
    Name = models.CharField(max_length=128, verbose_name=_("Name"))
    Value = models.CharField(max_length=128, verbose_name=_("Value"))
    Comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    objects = LabelManager()

    def __str__(self):
        return "{}:{}".format(self.Name, self.Value)

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Label')
