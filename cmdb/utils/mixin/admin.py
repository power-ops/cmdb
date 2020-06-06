from reversion.admin import VersionAdmin


class MixinAdmin(VersionAdmin):
    list_per_page = 30
    date_hierarchy = 'CreateDate'
    readonly_fields = ('CreateDate',)
