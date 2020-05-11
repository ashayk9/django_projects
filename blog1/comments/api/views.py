from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView
from comments.models import Comment
from . import serializers
from rest_framework import permissions
from posts.api.permissions import IsOwnerOrReadOnly
from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin


class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentListSerializer


class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    lookup_field = 'id'


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        model_type=self.request.GET.get("type")
        slug=self.request.GET.get("slug")
        parent_id=self.request.GET.get("parent_id", None)
        return serializers.create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )

class CommentEditView(DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentEditSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

