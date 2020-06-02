from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel


class LabelQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()


class LabelManager(models.Manager):
    def get_queryset(self):
        return LabelQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()


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
