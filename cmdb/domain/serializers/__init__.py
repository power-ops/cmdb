from django.urls import path
from .domain import DomainViewSet

urlpatterns = [
    path('domain/', DomainViewSet.as_view()),
    path('domain/<uuid:pk>/', DomainViewSet.as_view()),
]
