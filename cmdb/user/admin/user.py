from django.contrib import admin
from cmdb.mixin import MixinAdmin
from user import models, forms


@admin.register(models.User)
class UserAdmin(MixinAdmin):
    date_hierarchy = 'date_joined'
    readonly_fields = ('id', 'date_joined', 'last_login')

    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'last_login', 'is_active',
        'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    form = forms.UserForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = forms.UserChangForm
        return super().change_view(request, object_id, form_url, extra_context=extra_context, )
