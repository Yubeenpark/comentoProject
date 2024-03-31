from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm,GoogleProfileForm
from .models import Profile, Follow
from .google_oauth import *

import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests
from notifications import views as notification_views
from notifications.models import Notification

import logging

logger = logging.getLogger('__name__')

def signup(request):
    try:
        if request.method == 'POST':
            form = SignupForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                logger.debug('Sign up success  user id={}'.format(request.user.id))
                return redirect('accounts:login')
        else:
            form = SignupForm()
        return render(request, 'accounts/signup.html', {
            'form': form,
        })
    except Exception as e:
        logger.error('Exception={} while signup  '.format(e))

def login_check(request):
    try:
        if request.method == "POST":
            form = LoginForm(request.POST)
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            
            user = authenticate(username=name, password=pwd)
            
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(request, 'accounts/login_fail.html')
        else:
            form = LoginForm()
            return render(request, 'accounts/login.html', {"form":form})
    except Exception as e:
        logger.error('Exception={} while checking login'.format(e))

    
def logout(request):
    django_logout(request)
    return redirect("/")

@login_required
@require_POST
def follow(request):
    try:
        from_user = request.user.profile
        pk = request.POST.get('pk')
        to_user = get_object_or_404(Profile, pk=pk)
        follow, created = Follow.objects.get_or_create(from_user=from_user, to_user=to_user)
        
        if created:
            logger.debug('following success from user={}. to user={}'.format(request.user.id,to_user.user.id))
            message = '팔로우 시작!'
            notification_views.create_notification(request.user, to_user.user,'follow',follow.created_at)
            status = 1
        else:
            noti = get_object_or_404(Notification, creator=request.user,to=to_user.user,notification_type='follow')
            noti.delete()
            follow.delete()
            logger.debug('following cancel from user={}. to user={}'.format(request.user.id,to_user.user.id))
            message = '팔로우 취소'
            status = 0
            
        context = {
            'message': message,
            'status': status,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
    except Exception as e:
        logger.error('Exception={} while following'.format(e))


def google_login(request):
        if not(Profile.objects.filter(user=request.user).exists()):
            try:
                logger.debug('Google login success user id={}. But no Profile'.format(request.user.id))
                return redirect('accounts:google_signup')
            except Exception as e:
                logger.error('Exception={} while login google'.format(e))
        else:
            try:
                logger.debug('Google login success user id={}. Profile already exists'.format(request.user.id))
                return redirect('post:post_list')
            except Exception as e:
                logger.error('Exception={} while login google'.format(e))
        
        
def google_signup(request):
    if request.method == 'POST':
        try:
            form = GoogleProfileForm(request.POST, request.FILES,request=request)
            if form.is_valid():
                user = form.save()
                logger.info('Google signup by user={}. save user form'.format(request.user.id))
                return redirect('post:post_list')
        except Exception as e :
            logger.error('Exception={}, request={} while signup user id={}'.format(e,request,request.user.id))
        
    else:
        try:
            context = {'Googleform': GoogleProfileForm(request.POST, request.FILES, request=request)}
            return render(request, 'accounts/google_profile.html', context)
        except Exception as e :
            logger.error('Exception={}, request={} user id={} whle rendering google_profle page'.format(e,request,request.user.id))


