from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.db.models import Q
from reversion.admin import VersionAdmin
from asset import forms, models
from asset.models import Permission


@admin.register(models.Asset)
class AssetAdmin(VersionAdmin):
    list_display = ('Hostname', 'IP', 'get_protocols', 'Platform', 'Enabled', 'CreateDate')
    list_filter = ('Protocols', 'Labels', 'Platform')
    search_fields = ('Hostname', 'IP')
    form = forms.AssetForm
    fields = ['Hostname', 'IP', 'Protocols', 'Labels', 'Platform', 'Enabled', 'CreateDate']
    # list_editable = ('IP',)

    def has_view_permission(self, request, obj=None):
        """
        Return True if the given request has permission to view the given
        Django model instance. The default implementation doesn't examine the
        `obj` parameter.

        If overridden by the user in subclasses, it should return True if the
        given request has permission to view the `obj` model instance. If `obj`
        is None, it should return True if the request has permission to view
        any object of the given type.
        """
        opts = self.opts
        codename_view = get_permission_codename('view', opts)
        codename_change = get_permission_codename('change', opts)
        return (
                request.user.has_perm('%s.%s' % (opts.app_label, codename_view)) or
                request.user.has_perm('%s.%s' % (opts.app_label, codename_change)) or
                request.user.has_perm('%s.view_self_assets' % opts.app_label)
        )

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
