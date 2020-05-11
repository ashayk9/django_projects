from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST

from . serializers import UserCreateSerializer,UserLoginSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import serializers, permissions, response, status


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserLoginView(APIView):
    # queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data=request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # def post(self, request, format=None):
    #     data = request.data
    #
    #     username = data.get('username', None)
    #     password = data.get('password', None)
    #
    #     user = authenticate(username=username, password=password)
    #
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #
    #             return Response(status=status.HTTP_200_OK)
    #         else:
    #             return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #
