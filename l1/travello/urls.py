from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:primary_key>',views.individual_dest,name='place_details'),
]
