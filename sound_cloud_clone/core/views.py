from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from . models import Artist,Album,Song
from core.serializers import SongSerializer,AlbumSerializer,ArtistSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView


class SongGenericCreateView(CreateAPIView):
    queryset=Song.objects.all()
    serializer_class = SongSerializer

    def perform_create(self, serializer):
        serializer.save()


"""
class based view
get gives list of songs with their artists
post lets u create a new song
"""
class SongListView(APIView):

    def get(self,request):
        obj = Song.objects.all()
        serializer = SongSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        serializer = SongSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


"""
creates song using a function based view
"""
@csrf_exempt
def create_song(request):
    # obj = Artist.objects.get(artist_id=artist_id)
    # print(obj)
    # composer = Song.objects.get(artist_of_song=obj)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SongSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


"""
function based views
get gets detail of particular song
put to update a song
del to del a song
"""
@csrf_exempt
def detail(request,id):
    obj = Song.objects.get(id=id)

    if request.method=='GET':
        serializer = SongSerializer(obj)
        return JsonResponse(serializer.data)

    elif request.method=='PUT':
        data = JSONParser().parse(request)
        serializer = SongSerializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors)

    elif request.method=='DELETE':
        obj.delete()
        return Response(status=204)


class ArtistListView(APIView):

    def get(self,request):
        obj=Artist.objects.all()
        serializer = ArtistSerializer(obj, many=True)
        return Response(serializer.data)


class ArtistDetailView(APIView):
    def get(self, request, artist_id):
        obj = Artist.objects.get(artist_id=artist_id)
        print(obj)
        obj2 = Song.objects.filter(artist_of_song=obj)
        # obj2 = Song(artist_of_song=obj)
        serializer = ArtistSerializer(obj)
        serializer2 = SongSerializer(obj2,many=True)
        #serializer2 = SongSerializer(obj2)

        return Response(serializer2.data)

