from django.db import models
from django.utils.translation import ugettext_lazy as _
from cmdb.mixin import MixinUUIDModel, UUIDManager
from cmdb.utils import decrypt_ecb


class SystemUserQuerySet(models.QuerySet):
    pass


class SystemUserManager(UUIDManager):
    _queryset = SystemUserQuerySet


class SystemUser(MixinUUIDModel):
    Name = models.CharField(_('Name'), max_length=64, unique=True)
    Username = models.CharField(_('Username'), max_length=64)
    Password = models.TextField(_('Password'), null=True)
    LastPassword = models.TextField(_('Last Password'), null=True, default="")
    Key = models.BinaryField(_('Key'), null=True, default=None)
    Protocol = models.CharField(max_length=16, verbose_name=_('Protocol'))

    objects = SystemUserManager()

    def __str__(self):
        return self.Name

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
            "password": self.dpassword,
            "protocol": self.Protocol,
            "private_key": self.Key
        }

    @property
    def dpassword(self):
        if self.Password == "":
            return ""
        else:
            return decrypt_ecb(self.Password)

    class Meta:
        verbose_name = _('System User')
        verbose_name_plural = _('System User')

    # def save(self, *args, **kwargs):
    #     print(self)
    #     print(self.__class__)
    #     print(SystemUser)
    #     # cache.delete(self.__class__.__name__ + '.objects.all()')
    #     # super(SystemUser, self).save(*args, **kwargs)
    #     super(self.__class__, self).save(*args, **kwargs)
