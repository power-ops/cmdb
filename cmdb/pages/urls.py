from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import index, socketio
from .forms import CustomAuthForm

urlpatterns = [
    path('', index.ViewSet),
    path('test/', socketio.ViewSet),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ))
]
