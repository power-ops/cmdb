from django.urls import path
from .example import ExampleSearchView, ExampleViewSet

urlpatterns = [
    path('search', ExampleSearchView.as_view()),
    path('example_view/', ExampleViewSet.as_view()),
]
