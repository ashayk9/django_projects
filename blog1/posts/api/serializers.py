from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentDetailSerializer,CommentSerializer


post_detail_url=serializers.HyperlinkedIdentityField(
    view_name='detail_api',
    lookup_field='slug',
)


class PostListSerializer(serializers.ModelSerializer):
    url = post_detail_url
    user = serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields = [
            'user',
            'title',
            'url',
        ]

    def get_user(self,obj):
        return str(obj.user.username)


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields = [
            'user',
            'title',
            'slug',
            'content',
            'publish',
            'comments',
        ]

    def get_user(self,obj):
        return str(obj.user.username)

    def get_comments(self,obj):
        return CommentSerializer(obj.comments, many=True).data


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = [
            'title',
            'content',
            'publish',
        ]