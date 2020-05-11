from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Comment
from . forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect,Http404


def thread_comment_detail(request,id):
    obj=get_object_or_404(Comment,id=id)
    content_object=obj.content_object
    content_id=obj.object_id
    initial_data = {
        'content_type': obj.content_type,
        'object_id': obj.object_id
    }
    form=CommentForm(request.POST or None,initial=initial_data)
    if form.is_valid():
        print(form.cleaned_data)
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context={
        'c':obj,
        'form':form,
    }
    return render(request,'thread_detail.html', context=context)


def comment_del(request,id):
    obj=get_object_or_404(Comment,id=id)
    if obj.user != request.user:
        raise Http404
    if request.method=='POST':
        parent_obj_url = obj.content_object.get_absolute_url()
        messages.success(request,'sucessfully deleted')
        obj.delete()
        return HttpResponseRedirect(parent_obj_url)

    context={
        'obj':obj,
    }
    return render(request,'confirm_delete.html',context=context)
