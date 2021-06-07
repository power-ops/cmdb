from django.contrib.auth.models import Group as djGroup
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Group(djGroup):
    ExpireDate = models.DateTimeField(verbose_name=_('Expire Date'), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('User Group')
        verbose_name_plural = _('User Group')
        db_table = 'cmdb_group'
