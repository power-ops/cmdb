from django.contrib import admin
from asset import forms, models
from reversion.admin import VersionAdmin
from django.contrib.auth import get_permission_codename
from asset.models import Permission
from django.db.models import Q


@admin.register(models.AssetGroup)
class AssteGroupAdmin(VersionAdmin):
    list_display = ('Name', 'Enabled', 'CreateDate')
    form = forms.AssetForm
    readonly_fields = ('CreateDate',)
    fields = ['Name', 'Assets', 'Enabled', 'CreateDate']
    list_per_page = 30

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
            request.user.has_perm('asset.view_self_assets')
        )

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        if request.user.has_perm('asset.view_self_assets') and not request.user.has_perm('assetgroup.view_asset'):
            List = []
            for res in Permission.objects.filter(
                Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(User=request.user.id)):
                List += list(res.AssetGroup.values_list('uuid', flat=True))
            List = list(set(List))
            qs = qs.filter(uuid__in=List)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
