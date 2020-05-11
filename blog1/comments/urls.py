from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>',views.thread_comment_detail,name='thread_detail'),
    path('delete/<int:id>',views.comment_del,name='thread_del'),
]