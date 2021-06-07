from reversion.admin import VersionAdmin


class MixinAdmin(VersionAdmin):
    list_per_page = 30
    date_hierarchy = 'CreateDate'

    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        if not self.readonly_fields:
            if hasattr(self.model, 'id'):
                self.readonly_fields = ('id', 'CreateDate',)
            elif hasattr(self.model, 'uuid'):
                self.readonly_fields = ('uuid', 'CreateDate',)
        super().__init__(model, admin_site)
