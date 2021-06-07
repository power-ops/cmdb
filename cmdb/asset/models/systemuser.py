from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from management.mixins import MixinUUIDModel, UUIDManager
from management.utils.password import decrypt_ecb, encrypt_ecb
from asset.models import Protocol


class SystemUserQuerySet(models.QuerySet):
    pass


class SystemUserManager(UUIDManager):
    _queryset = SystemUserQuerySet


class SystemUser(MixinUUIDModel):
    Name = models.CharField(_('Name'), max_length=64, unique=True)
    Username = models.CharField(_('Username'), max_length=64)
    Password = models.TextField(_('Password'), null=True)
    LastPassword = models.TextField(_('Last Password'), null=True, default="")
    Key = models.TextField(_('Key'), null=True)
    Protocols = models.ManyToManyField(Protocol, verbose_name=_('Protocol'))

    objects = SystemUserManager()

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = _('System User')
        verbose_name_plural = _('System User')

    def update_password(self, password, safe=True):
        if safe:
            self.LastPassword = self.Password
        self.Password = password
        self.save()

    def json(self):
        return {
            "name": self.Name,
            "username": self.Username,
            "password": self.Password,
            "protocol": self.Protocol,
            "key": self.Key
        }

    def xjson(self):
        return {
            "id": self.uuid,
            "name": self.Name,
            "username": self.Username,
            "password": self.dPassword,
            "protocol": self.Protocol,
            "private_key": self.dKey
        }

    @property
    def dPassword(self):
        if self.Password == "":
            return ""
        else:
            return decrypt_ecb(self.Password)

    @property
    def dKey(self):
        if self.Key == "":
            return ""
        else:
            return decrypt_ecb(self.Key)

    def save(self, *args, **kwargs):
        if self.Password or self.Key:
            oj = SystemUser.objects.get_by_id(self.uuid)
            if self.Password and ((not oj) or (oj.Password != self.Password)):
                self.Password = encrypt_ecb(self.Password)
            if self.Key and ((not oj) or (oj.Key != self.Key)):
                self.Key = encrypt_ecb(self.Key)
        if not self._cache_all_bypass:
            cache.delete(self.__class__.__name__ + '.objects.all()')
        super(SystemUser, self).save(*args, **kwargs)

    def get_protocols(self):
        return [p.__str__() for p in self.Protocols.all()]

    get_protocols.short_description = _('Protocols')
