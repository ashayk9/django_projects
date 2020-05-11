from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView
from django.http import HttpResponseRedirect
from . forms import PostForm
from . models import Post
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.http import Http404
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#
#     def test_func(self):
#         return self.request.user.is_superuser or self.request.user.is_staff


def post(request):
    return render(request,'base.html',{})


# class PostList(ListView):
#     model = Post
#     template_name = 'post_list.html'
#     context_object_name = 'items'
#
#     queryset = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())
def post_list(request):
    if request.user.is_staff or request.user.is_superuser:
        queryset= Post.objects.all()
    else:
        queryset = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())
    context={
        'items':queryset
    }
    return render(request,'post_list.html',context=context)


def detail_view(request, slug=None):

    obj = get_object_or_404(Post, slug=slug)
    if obj.publish>timezone.now().date() or obj.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    # content_type = ContentType.objects.get_for_model(Post)
    # object_id = obj.id
    # comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
    comments = obj.comments
    # comments=Comment.objects.filter_by_instance(instance=obj)
    initial_data={
        'content_type': obj.get_content_type,
        'object_id': obj.id
    }
    form=CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        print(form.cleaned_data)
        c_type=form.cleaned_data.get('content_type')
        content_type=ContentType.objects.get(model=c_type)
        obj_id=form.cleaned_data.get('object_id')
        content_data=form.cleaned_data.get('content')
        parent_obj=None
        try:
            parent_id=int(request.POST.get('parent_id'))
        except:
            parent_id=None

        if parent_id:
            parent_qs=Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                print(parent_qs)
                parent_obj=parent_qs.first()

        new_comment, created=Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        'obj':obj,
        'comments':comments,
        'comment_form':form,
    }

    return render(request,'post_detail.html',context=context)


# class PostCreate(View,UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser or self.request.user.is_staff
#
#     def get(self,*args,**kwargs):
#         form=PostForm()
#         context={
#             'form':form
#         }
#         return render(self.request, 'post_form.html',context=context)
#
#     def post(self,*args,**kwargs):
#         form=PostForm(self.request.POST or None)
#         if form.is_valid():
#             instance = form.save()
#             instance.save()
#             context = {
#                 'form': form
#             }
#             return redirect('list')

def create_view(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method=='POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
        context = {
            'form': form
        }
        return redirect('list')
    form=PostForm()
    context={
        'form':form
    }
    return render(request, 'post_form.html',context=context)







def post_update_view(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = get_object_or_404(Post, id=id)
    form=PostForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('list')
    context={
        'obj':obj,
        'form':form
    }

    return render(request,'post_form.html',context=context)

def delete_view(request, id):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    return redirect('list')

def pre_save_post_reciever(sender, instance,*args,**kwargs):
    slug=slugify(instance.title)
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" %(slug, instance.id)

    instance.slug=slug

pre_save.connect(pre_save_post_reciever, sender=Post)



