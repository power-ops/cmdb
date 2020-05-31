from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.mixin import MixinModel
from utils.password import encrypt_ecb, decrypt_ecb, gen


class SystemUserQuerySet(models.QuerySet):
    pass


class SystemUserManager(models.Manager):
    def get_queryset(self):
        return SystemUserQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        return self.get_queryset().filter(uuid=id).first()


class SystemUser(MixinModel):
    BASE_CHOICES = (
        ('empty', 'empty'),
        ('create_pwd', 'create_pwd'),
        ('create_key', 'create_key'),
        ('inherit', 'inherit'),
    )
    Name = models.CharField(_('Name'), max_length=64, unique=True)
    Username = models.CharField(_('Username'), max_length=64)
    Password = models.TextField(_('Password'), null=True)
    LastPassword = models.TextField(_('Last Password'), null=True, default="")
    Key = models.BinaryField(_('Key'), null=True, default=None)
    Protocol = models.CharField(max_length=16, verbose_name=_('Protocol'))
    Jid = models.CharField(max_length=64, verbose_name=_('jid'), null=True, default="")
    Type = models.CharField(choices=BASE_CHOICES, max_length=16, default="empty")
    objects = SystemUserManager()

    def __str__(self):
        return self.Name

    def update_password(self, password, safe=True):
        if safe:
            self.LastPassword = self.Password
        self.Password = password
        self.save()

    def me(self, Username, domain=None):
        if domain:
            Username = Username + "@" + domain
        SU = SystemUser.objects.filter(Name=self.Name + "_U:" + Username + '_P:' + self.Protocol).first()
        if not SU:
            SU = SystemUser.objects.create(
                Name=self.Name + "_U:" + Username + '_P:' + self.Protocol,
                Username=Username,
                Protocol=self.Protocol,
                Type=self.Type
            )
            if self.Type == "empty":
                pass
            elif self.Type == "create_pwd":
                SU.Password = encrypt_ecb(gen())
            elif self.Type == "create_key":
                SU.Key = ""  # todo
            elif self.Type == "inherit":
                SU.Password = self.Password
                SU.Key = self.Key
            SU.save()
        return SU

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
        # db_table = 'SystemUser'
        verbose_name = _('SystemUser')
        verbose_name_plural = _('SystemUser')
