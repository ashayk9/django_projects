from django.urls import path
from . import views

urlpatterns = [
    path('',views.CommentListView.as_view(),name='comment_list_api'),
    path('<int:id>',views.CommentDetailView.as_view(),name='comment_detail_api'),
    path('<int:id>/edit', views.CommentEditView.as_view(), name='comment_edit_api'),
    path('create/',views.CommentCreateView.as_view(),name='create_api'),
]