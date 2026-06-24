from django.urls import path

from .views import LoginView, UserListCreateView

urlpatterns = [
    path('auth/login', LoginView.as_view()),
    path('users', UserListCreateView.as_view()),
]
