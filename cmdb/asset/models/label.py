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
    # SYSTEM_CATEGORY = "S"
    # USER_CATEGORY = "U"
    # CATEGORY_CHOICES = (
    #     ("S", _("System")),
    #     ("U", _("User"))
    # )
    Name = models.CharField(max_length=128, verbose_name=_("Name"))
    Value = models.CharField(max_length=128, verbose_name=_("Value"))
    # Category = models.CharField(max_length=128, choices=CATEGORY_CHOICES,
    #                             default=USER_CATEGORY, verbose_name=_("Category"))
    Comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    objects = LabelManager()

    # @classmethod
    # def get_queryset_group_by_name(cls):
    #     names = cls.objects.values_list('name', flat=True)
    #     for name in names:
    #         yield name, cls.objects.filter(Name=name)

    def __str__(self):
        return "{}:{}".format(self.Name, self.Value)

    class Meta:
        # db_table = "assets_label"
        unique_together = [('Name', 'Value')]
