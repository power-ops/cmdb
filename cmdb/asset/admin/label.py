from django.contrib import admin
from asset import models
from asset.models import Permission
from asset.mixin import MixinAdmin


@admin.register(models.Label)
class LabelAdmin(MixinAdmin):
    fields = ['Name', 'Value', 'Enabled', 'CreateDate']
    list_display = ['Name', 'Value', 'Enabled', 'CreateDate']

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        if request.user.has_perm('asset.view_self_assets') and not request.user.has_perm('label.view_label'):
            List = []
            for res in Permission.objects.UserAssets(request.user):
                List += list(res.Labels.values_list('uuid', flat=True))
            List = list(set(List))
            qs = qs.filter(uuid__in=List)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
