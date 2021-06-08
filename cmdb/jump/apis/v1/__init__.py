from django.urls import path
from .token import TokenCreateView, TokenView

urlpatterns = [
    path('token', TokenCreateView.as_view()),
    path('token/<str:pk>', TokenView.as_view()),
]
