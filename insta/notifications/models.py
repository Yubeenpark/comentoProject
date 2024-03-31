from django.core.exceptions import FieldError
from django.conf import settings
from django.db import models
from accounts.models import Profile as user_model
from post.models import Post as post_model

# Create your models here.

class Notification(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='to')
    TYPE_CHOICES = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('follow', 'follow')    
    )
    notification_type  = models.CharField(max_length=200, choices=TYPE_CHOICES,default='N')
    #image = models.ImageField( null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    comment= models.CharField(max_length=40, null=True,blank=True)

    class Meta:
        ordering = ['-created_at']
    

  