from rest_framework import serializers
from comments.models import Comment,CommentManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

comment_detail_url=serializers.HyperlinkedIdentityField(
    view_name='comment_detail_api',
    lookup_field='id',
)


class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model=Comment
        fields = [
            'id',
            'user',
            'content_type',
            'object_id',
            'content',
            'reply_count',
            'timestamp',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_reply_count(self,obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    # def get_replies(self, obj):
    #     if obj.is_parent:
    #         return CommentChildSerializer(obj.children(), many=True).data
    #     return None


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model=Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'user',
            'timestamp',
            'replies',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    content_obj_url = serializers.SerializerMethodField()
    url = comment_detail_url
    class Meta:
        model=Comment
        fields = [
            'id',
            'user',
            # 'content_type',
            # 'object_id',
            'content',
            'url',
            # 'parent',
            'timestamp',
            'reply_count',
            'content_obj_url',
        ]
    def get_user(self, obj):
        return str(obj.user.username)

    def get_reply_count(self,obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    def get_content_obj_url(self,obj):
        return obj.content_object.get_api_url()

def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):

    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields=[
                'id',
                'content',
                'timestamp',
            ]

        def __init__(self, *args, **kwargs):
            #super().__init__(**kwargs)
            self.model_type=model_type
            self.slug=slug
            self.parent_obj=None
            if parent_id:
                parent_qs=Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    self.parent_obj=parent_qs.first()

            super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count()!=1:
                raise serializers.ValidationError("this slug does not belong to the content type")
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            #user = validated_data.get('user')

            user=User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj=self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type,
                slug,
                content,
                user,
                parent_obj=parent_obj,
            )
            return comment
    return CommentCreateSerializer


class CommentEditSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model=Comment
        fields = [
            'id',
            'content',
            'user',
            'replies',
        ]
        read_only_fields=['replies']

    def get_user(self, obj):
        return str(obj.user.username)

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None