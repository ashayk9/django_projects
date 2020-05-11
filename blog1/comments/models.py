from django.db import models
from django.contrib.auth.models import User
#from posts.models import Post
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        qs=super(CommentManager,self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type,slug,content,user,parent_obj):
        model_qs=ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists():
                instance=self.model()
                instance.content=content
                instance.user=user
                instance.content_type=model_qs.first()
                instance.object_id=obj_qs.first().id
                if parent_obj:
                    instance.parent=parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    #post=models.ForeignKey(Post)
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    objects=CommentManager()

    parent=models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering= ['-timestamp']

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse("thread_detail",kwargs={'id':self.pk})

    # def get_api_url(self):
    #     return reverse("comment_detail_api",kwargs={'id':self.pk})

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True