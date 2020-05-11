from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView
from posts.models import Post
from . import serializers
from rest_framework import permissions
from . permissions import IsOwnerOrReadOnly



class PostListView(ListAPIView):
    queryset=Post.objects.all()
    serializer_class = serializers.PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset=Post.objects.all()
    serializer_class = serializers.PostDetailSerializer
    lookup_field = 'slug'

class PostUpdateView(UpdateAPIView):
    queryset=Post.objects.all()
    serializer_class = serializers.PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDeleteView(DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class = serializers.PostDetailSerializer
    lookup_field = 'slug'

class PostCreatelView(CreateAPIView):
    queryset=Post.objects.all()
    serializer_class = serializers.PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

