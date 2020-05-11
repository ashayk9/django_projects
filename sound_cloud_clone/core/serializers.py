from  rest_framework import serializers
from . models import Artist,Album,Song


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            'name'
        ]


class SongSerializer(serializers.ModelSerializer):
    # artist_of_song=serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = [
            'title','artist_of_song'
        ]
    # def get_artist_of_song(self, obj):
    #     return str(obj.artist_of_song.name)


