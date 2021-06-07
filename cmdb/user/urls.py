from django.urls import path
from .views import createsuperuser

urlpatterns = [
    path('createsuperuser/', createsuperuser),
]
