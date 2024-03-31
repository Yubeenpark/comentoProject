from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from notifications.models import Notification
import logging

logger = logging.getLogger('__name__')

@login_required
def get_notification(request):
    try:
        
        print('noti')
        try:
            noti = Notification.objects.filter(to=request.user)
            print(noti)
            
            return render(request, 'layout.html', {
            'noti':noti,
            'length':len(noti),
        })
        except Notification.DoesNotExist:
            return render(request, 'layout.html')
        
    except Exception as e :
         logger.error('Exception={} while get notification  '.format(e))

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),    

    path('post/', include('post.urls', namespace='post')),
    path('', lambda r: redirect('post:post_list'), name='root'),
    path('chat/', include('chat.urls')),
    path("notifications/", include('notifications.urls', namespace="notifications")),
    path('noti/', get_notification,name='noti'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns


