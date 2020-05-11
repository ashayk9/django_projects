from django.urls import path
from . import views
from posts.models import Post
from . import serializers

urlpatterns = [
    path('create',views.PostCreatelView.as_view(), name='create_api'),
    path('',views.PostListView.as_view(),name='list_api'),
    path('<slug>',views.PostDetailView.as_view(),name='detail_api'),
    path('<slug>/edit',views.PostUpdateView.as_view(), name='update_api'),
    path('<slug/delete>',views.PostDeleteView.as_view(), name='detail_api'),



]