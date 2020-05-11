from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('add', views.add, name='add'),
    ]
