from django.contrib import admin
from django.db.models import Q
from asset import forms, models
from asset.models import Permission
from asset.mixin import MixinAdmin


@admin.register(models.Asset)
class AssetAdmin(MixinAdmin):
    # prepopulated_fields = {'Platform': ('Name',)}
    raw_id_fields = ("Platform",)
    list_display = ('Hostname', 'IP', 'get_protocols', 'Platform', 'Enabled', 'CreateDate')
    list_filter = ('Protocols', 'Labels', 'Platform')
    search_fields = ('Hostname', 'IP')
    form = forms.AssetForm
    fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled', 'CreateDate']

    # list_editable = ('IP',)

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        if request.user.has_perm('asset.view_self_assets') and not request.user.has_perm('asset.view_asset'):
            Assets = []
            for res in Permission.objects.filter(
                Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(User=request.user.id)):
                for asset in res.Asset.all():
                    if asset.uuid not in Assets:
                        Assets.append(asset.uuid)
                for assetGroup in res.AssetGroup.all():
                    for asset in assetGroup.Assets.all():
                        if asset.uuid not in Assets:
                            Assets.append(asset.uuid)
            qs = qs.filter(uuid__in=Assets)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
