from django.urls import path
from .views import *
from django.conf.urls import url, include

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_check, name='login'),
    path('logout/', logout, name='logout'),
    path('follow/', follow, name='follow'),
    path('google/',google_login,name='google'),
    path('google/signup',google_signup,name='google_signup'),
    #path('', include('social_django.urls', namespace='social')),
    path('', include('social_django.urls', namespace='social')),
]