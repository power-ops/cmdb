from django.db import models


class MixinQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)
