from django.contrib import admin
from django.db.models import Q
from asset.models import Permission
from asset import forms, models
from asset.mixin import MixinAdmin


@admin.register(models.SystemUser)
class SystemUserAdmin(MixinAdmin):
    list_display = ('Name', 'Username', 'get_protocols', 'Enabled', 'CreateDate')
    form = forms.SystemUserForm
    readonly_fields = ('CreateDate', 'LastPassword')

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        if request.user.has_perm('asset.view_self_assets') and not request.user.has_perm('systemuser.view_systemuser'):
            List = []
            for res in Permission.objects.filter(
                    Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(User=request.user.id)):
                List += list(res.SystemUser.values_list('uuid', flat=True))
            List = list(set(List))
            qs = qs.filter(uuid__in=List)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
