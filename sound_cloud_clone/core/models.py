from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name=models.CharField(max_length=30)
    artist_id = models.IntegerField()
    # user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Song(models.Model):
    title=models.CharField(max_length=20)
    # artist_of_song = models.ForeignKey('Artist',on_delete=models.SET_NULL, null=True)
    artist_of_song = models.ManyToManyField(Artist)

    def __str__(self):
        return self.title


class Album(models.Model):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    album_tite = models.CharField(max_length=20)
    # artist_of_album = models.ForeignKey('Artist',on_delete=models.SET_NULL, null=True)
    # artist_of_album = models.ManyToManyField('Artist')

    def __str__(self):
        return self.album_tite


