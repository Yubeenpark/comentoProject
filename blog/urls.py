from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='index'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('post/create/',views.post_create, name='post_create'),
    path('<int:post_id>/delete/',views.post_delete, name='post_delete'),
    path('post/modify/<int:post_id>/', views.post_modify, name='post_modify'),

]