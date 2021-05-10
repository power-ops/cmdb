from django.urls import path
from .token import TokenView

urlpatterns = [
    path('token', TokenView.as_view()),
]
