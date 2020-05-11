from django.urls import path
from . import views

urlpatterns = [
    #path('',views.post, name='post'),
    #path('create', views.PostCreate.as_view(),name='create'),
    path('create',views.create_view,name='create'),
    #path('list',views.PostList.as_view(), name='list'),
    path('',views.post_list,name='list'),
    path('details/<slug>', views.detail_view, name='details'),
    path('update/<int:id>',views.post_update_view, name='update'),
    path('delete/<int:id>', views.delete_view, name='delete'),


]