from rest_framework import serializers
from .models import Notification

#from insta.post import serializers as image_serializers

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'