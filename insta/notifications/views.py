from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from django.shortcuts import get_object_or_404,render
from django.contrib.auth import get_user_model
from .models import Notification
import logging

logger = logging.getLogger(__name__)

class Notifications(APIView):
    
    def get(self, request, format=None):
    
        user = request.user
        notifications = models.Notification.objects.filter(to=user)

        serializer = serializers.NotificationSerializer(notifications, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

def create_notification(creator, to, notification_type,created_at,comment=None):
    
    notification = Notification.objects.create(
        creator = creator,
        to = to,
        notification_type = notification_type,
        created_at=created_at,
        comment=comment

    )

    notification.save()
