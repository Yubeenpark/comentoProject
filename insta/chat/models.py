from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from accounts.models import Profile
from chat.utils import MessageIndex

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_messages',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]


    def indexing(self):
        obj = MessageIndex(
            meta={'id': self.id},
            timestamp=self.timestamp,
            author=self.author.id,
            content=self.content,
            )
        obj.save()
        return obj
