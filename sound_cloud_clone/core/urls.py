from django.urls import path
from . import views

urlpatterns = [

    path('',views.SongListView.as_view(),name='song_list'),
    path('generic',views.SongGenericCreateView.as_view()),
    path('songs/<id>',views.detail),
    path('artists',views.ArtistListView.as_view(),name='artist_list'),
    path('artists/<artist_id>',views.ArtistDetailView.as_view()),
    path('create', views.create_song, name='create'),
]