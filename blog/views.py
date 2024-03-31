
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostingForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse

def post_list(request):
    """
    * main *
    show post list 
    """
    posts = Post.objects.all()
    if 'page' in request.GET:
        p = int(request.GET['page'])
        posts = posts[(p - 1) * 10, p * 10]
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, post_id):
    """
    show detail page about post clicked
    """
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'blog/post_detail.html', context)

@login_required(login_url='/common/login/')
def post_create(request):
    """
    create new posting 
    """
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('blog:index')
    else:
        form = PostingForm()
    context = {'form': form}
    return render(request, 'blog/post_create.html', context)


def post_delete(request,post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.delete()
        return render(request, 'blog/post_delete.html')

    elif request.method == 'GET':
        return HttpResponse('잘못된 접근 입니다.')


def post_modify(request, post_id):
    """
    질문수정
    """
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('blog:detail', post_id=post.id)

    if request.method == "POST":
        form = PostingForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.modify_date = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('blog:detail', post_id=post.id)
    else:
        form = PostingForm(instance=post)
    context = {'form': form}
    return render(request, 'blog/post_create.html', context)


