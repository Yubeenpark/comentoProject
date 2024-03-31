import json
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, response
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import PostForm, CommentForm
from .models import Post, Like, Comment, Tag
from django.db.models import Count
from notifications import views as notification_views
import logging
from notifications.models import Notification

logger = logging.getLogger(__name__)

def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm()
        logger.info('user={} click post={}'.format(request.user.id,post.id))
        return render(request, 'post/post_detail.html', {
            'comment_form': comment_form,
            'post': post,
        })
    except Exception as e :
            logger.error('Exception={}, request={}, pk={} while seeing post detail'.format(e,request,pk))


def my_post_list(request, username):
    try:
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile

        target_user = get_user_model().objects.filter(id=user.id).select_related('profile') \
            .prefetch_related('profile__follower_user__from_user', 'profile__follow_user__to_user')

        post_list = user.post_set.all()

        all_post_list = Post.objects.all()
        noti = Notification.objects.filter(to=request.user)
        
        return render(request, 'post/my_post_list.html', {
            'user_profile': user_profile,
            'target_user': target_user,
            'post_list': post_list,
            'all_post_list': all_post_list,
            'username': username,
            'noti':noti,
            'length':len(noti),
        })
    except Exception as e:
        logger.error('Exception={}, request={}, pk={} while loading user={} post-list'.format(e,request,username))


def post_list(request, tag=None):
    tag_all = Tag.objects.annotate(num_post=Count('post')).order_by('-num_post')

    if tag:
        post_list = Post.objects.filter(tag_set__name__iexact=tag) \
            .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                              'author__profile__follower_user', 'author__profile__follower_user__from_user') \
            .select_related('author__profile')
    else:
        post_list = Post.objects.all() \
            .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                              'author__profile__follower_user', 'author__profile__follower_user__from_user') \
            .select_related('author__profile')

    comment_form = CommentForm()

    paginator = Paginator(post_list, 3)
    page_num = request.POST.get('page')

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, 'post/post_list_ajax.html', {
            'posts': posts,
            'comment_form': comment_form,
        })


    noti = Notification.objects.filter(to=request.user)

    if request.method == 'POST':
        tag = request.POST.get('tag')
        tag_clean = ''.join(e for e in tag if e.isalnum())
        return redirect('post:post_search', tag_clean)

    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        follow_set = request.user.profile.get_following
        follow_post_list = Post.objects.filter(author__profile__in=follow_set)

        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'tag': tag,
            'posts': posts,
            'follow_post_list': follow_post_list,
            'comment_form': comment_form,
            'tag_all': tag_all,
            'noti':noti,
            'length':len(noti),
        })
    else:
        return render(request, 'post/post_list.html', {
            'tag': tag,
            'posts': posts,
            'comment_form': comment_form,
            'tag_all': tag_all,
            'noti':noti,
            'length':len(noti),
        })


@login_required
def post_new(request):
    try:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                post.tag_save()
                logger.info('user={} write new post={}'.format(request.user.id,post.id))
                messages.info(request, '새 글이 등록되었습니다')
                return redirect('post:post_list')
        else:
            form = PostForm()
        noti = Notification.objects.filter(to=request.user)
        return render(request, 'post/post_new.html', {
            'form': form,
            'noti':noti,
            'length':len(noti),
        })
    except Exception as e:
        logger.error('Exception={}, request user={} while creating new post'.format(e,request.user))



@login_required
def post_edit(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            messages.warning(request, '잘못된 접근입니다')
            return redirect('post:post_list')

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                post.tag_set.clear()
                post.tag_save()
                logger.info('user={}  edit post={}'.format(request.user.id,post.id))
                messages.success(request, '수정완료')
                return redirect('post:post_list')
        else:
            form = PostForm(instance=post)
        return render(request, 'post/post_edit.html', {
            'post': post,
            'form': form,
        })
    except Exception as e:
        logger.error('Exception={}, request user={} while editing post'.format(e,request.user))



@login_required
@require_POST
def post_like(request):
    try:
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)
        post_like, post_like_created = post.like_set.get_or_create(user=request.user)
        
        if not post_like_created:
            noti = get_object_or_404(Notification, creator=request.user,to=post.author,notification_type='like',created_at=post_like.created_at)
            post_like.delete()
            noti.delete()
            logger.info('user={} cancel liking post={}'.format(request.user.id,post.id))
            message = "좋아요 취소"
        else:
            logger.info('user={} like post={}'.format(request.user.id,post.id))
            message = "좋아요"
            notification_views.create_notification(request.user, post.author, 'like', post_like.created_at)
            
        

        context = {'like_count': post.like_count,
                'message': message}

        return HttpResponse(json.dumps(context), content_type="application/json")
    except Exception as e:
        logger.error('Exception={}, request user={} while liking post'.format(e,request.user))



@login_required
@require_POST
def post_bookmark(request):
    try:
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)
        post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(user=request.user)

        if not post_bookmark_created:
            post_bookmark.delete()
            logger.info('user={} cancel bookmarking post={}'.format(request.user.id,post.id))
            message = "북마크 취소"
        else:
            logger.info('user={} bookmark post={}'.format(request.user.id,post.id))
            message = "북마크"

        context = {'bookmark_count': post.bookmark_count,
                'message': message}

        return HttpResponse(json.dumps(context), content_type="application/json")
    except Exception as e:
        logger.error('Exception={}, request user={} while bookmarking post'.format(e,request.user))



@login_required
def post_delete(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user or request.method == 'GET':
            logger.warning('user={} cannot delete post={}. Because post author is {} '.format(request.user.id,post.id,post.author))
            messages.warning(request, '잘못된 접근입니다.')
            return redirect('post:post_list')

        if request.method == 'POST':
            post.delete()
            logger.debug('user={} delete post={}.'.format(request.user.id,post.id))
            # messages.success(request, '삭제완료')
            return redirect('post:post_list')
    except Exception as e:
        logger.error('Exception={}, request user={} while delete post'.format(e,request.user))



@login_required
def comment_new(request):
    try:
        print("comment_new")
        pk = request.POST.get('pk')
        content = request.POST.get('content')
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            print('post')
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)

                comment.author = request.user
                comment.post = post
                comment.save()
                text = comment.content
                if(text.find('@') != -1):
                    print('@찾았음')
                logger.debug('user={} create comment to post={}.'.format(request.user,post.id))
                
                noti=notification_views.create_notification(request.user, post.author, 'comment',comment.created_at,comment.content)
                return render(request, 'post/comment_new_ajax.html', {
                    'comment': comment,
                })
        return redirect("post:post_list")
    except Exception as e:
        logger.error('Exception={} while creating new comment'.format(e))


@login_required
def comment_new_detail(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            logger.debug('user={} create comment={} detail to post={}.'.format(request.user,comment.content,comment.post))
            return render(request, 'post/comment_new_detail_ajax.html', {
                'comment': comment,
            })


@login_required
def comment_delete(request):
    try:
        pk = request.POST.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        #print(comment.post.author,'   ',comment.author, comment.created_at)
        noti = get_object_or_404(Notification, creator=comment.author,to=comment.post.author,notification_type='comment',created_at=comment.created_at,comment=comment.content)


        if request.method == 'POST' and request.user == comment.author:
            comment.delete()
            noti.delete()
            logger.debug('user={} delete comment in post={}.'.format(request.user,comment.id,comment.post))
            message = '삭제완료'
            status = 1

        else:
            logger.warning('user={} cannot delete comment={}. Because comment author is {} '.format(request.user.id,comment.id,comment.author))
            message = '잘못된 접근입니다'
            status = 0

        return HttpResponse(json.dumps({'message': message, 'status': status, }), content_type="application/json")
    except Exception as e:
        logger.error('Exception={} while deleteing comment and notification'.format(e))
