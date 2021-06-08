from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from management.settings.file_storage import FileStorage


class User(AbstractUser):
    # todo: change the storage path with username
    avatar = models.ImageField(storage=FileStorage(location=settings.AVATAR), null=True)
    language = models.CharField(max_length=8, choices=settings.LANGUAGES, default='en')
    publicKey = models.TextField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')
        db_table = 'cmdb_user'
