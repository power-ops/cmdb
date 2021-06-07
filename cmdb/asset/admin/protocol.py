from django.contrib import admin
from asset import models
from asset.mixin import MixinAdmin


@admin.register(models.Protocol)
class ProtocolAdmin(MixinAdmin):
    fields = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']
    list_display = ['Name', 'Protocol', 'Port', 'Enabled', 'CreateDate']

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        if request.user.has_perm('asset.view_self_assets') and not request.user.has_perm('protocol.view_protocol'):
            List = []
            for res in models.Permission.objects.UserAssets(request.user):
                List += list(res.Protocols.values_list('uuid', flat=True))
            List = list(set(List))
            qs = qs.filter(uuid__in=List)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
