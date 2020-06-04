from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinUUIDModel


class Platform(MixinUUIDModel):
    Name = models.SlugField(verbose_name=_("Name"), unique=True, allow_unicode=True)
    Comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    @classmethod
    def init(self):
        for base in ['Linux', 'Unix', 'Darwin', 'BSD', 'Windows', 'Workplace', 'Other']:
            self.objects.get_or_create(
                Name=base, Comment=''
            )

    @classmethod
    def default(self):
        linux, created = self.objects.get_or_create(
            Name='Linux', Comment=''
        )
        return linux.uuid

    def is_windows(self):
        return self.Name.lower() in ('windows',)

    def is_unixlike(self):
        return self.Name.lower() in ("linux", "unix", "darwin", "bsd")

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = _("Platform")
        verbose_name_plural = _('Platform')
