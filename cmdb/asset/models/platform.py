from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinModel


class Platform(MixinModel):
    Name = models.SlugField(verbose_name=_("Name"), unique=True, allow_unicode=True)
    Comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = _("Platform")
        verbose_name_plural = _('Platform')

    @classmethod
    def default(self):
        linux, created = self.objects.get_or_create(
            Name='Linux', Comment=''
        )
        return linux.pk

    def is_windows(self):
        return self.Name.lower() in ('windows',)

    def is_unixlike(self):
        return self.Name.lower() in ("linux", "unix", "darwin", "bsd")
