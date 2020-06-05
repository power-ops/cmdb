from django.db import models


class MixinQuerySet(models.QuerySet):
    def active(self):
        return self.filter(Enabled=True)

    def valid(self):
        return self.active()
