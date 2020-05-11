from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserCreateView.as_view(), name='api_register'),
    path('login', views.UserLoginView.as_view(), name='api_login'),
]