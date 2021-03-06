from django.contrib import admin
from asset import forms, models
from asset.models import Permission
from django.db.models import Q
from asset.mixin import MixinAdmin


@admin.register(models.AssetGroup)
class AssteGroupAdmin(MixinAdmin):
    list_display = ('Name', 'Enabled', 'CreateDate')
    form = forms.AssetGroupForm
    fields = ['Name', 'Assets', 'Enabled', 'CreateDate']

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
