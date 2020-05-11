from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)
    publish = models.DateField(auto_now_add=False, auto_now=False)
    draft = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("details",kwargs={'slug':self.slug})

    def get_api_url(self):
        return reverse("detail_api",kwargs={'slug':self.slug})

    @property
    def comments(self):
        instance=self
        qs=Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance=self
        content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type



