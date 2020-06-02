from django.contrib import admin
from asset import forms, models
from reversion.admin import VersionAdmin
from django.contrib.auth import get_permission_codename
from asset.views import getSelfAssets


@admin.register(models.Protocol)
class ProtocolAdmin(VersionAdmin):
    fields = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']
    readonly_fields = ['CreateDate']
    list_display = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']

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
        if request.user.has_perm('asset.view_self_assets') and not request.user.has_perm('protocol.view_protocol'):
            List = []
            for res in getSelfAssets(request):
                List += list(res.Protocols.values_list('uuid', flat=True))
            List = list(set(List))
            qs = qs.filter(uuid__in=List)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
