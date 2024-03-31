from django.db.models.fields import NullBooleanField
from .serializers import MessageSerializer
from .models import Message
import json
from django.forms.models import model_to_dict
from django.core.checks import messages
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from . import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
import json
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        try: 
            messages = Message.last_10_messages()
            content = {
            'messages': self.messages_to_json(messages)
                }
            self.send_chat_message(content)
        except Exception as e:
            logger.error('Exception={} room_name={} author={} while fetching messages '.format(e,self.room_name,data['from']))


    def new_message(self, data):
        try:
            author = data['from']
            author_user = User.objects.filter(username=author)[0]
            message = Message.objects.create(
                author=author_user,
                content=data['message'],
                )
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
            logger.info('User id={} send new mesaage={}'.format(author_user.id,data['message']))
            return self.send_chat_message(content)
        except Exception as e:
            logger.error('Exception={} author={} message={} while receiving new messages '.format(e,data['from'],data['message']))

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        if message is NullBooleanField:
            print('null')
        return {
            'author': message.author.username,
            'nickname': message.author.profile.nickname,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'picture': message.author.profile.picture.url,
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }
    
    
    def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
                )
            self.accept()
            logger.info('room name={}, group name={} was connected'.format(self.room_name, self.room_group_name))
        except Exception as e:
            logger.error('Exception={}, room_name={}, channel name={} while connecting room '.format(e,self.channel_name,self.room_name))


    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        except Exception as e :
            logger.error('Exception={}, close code={} while disconnecting room={} '.format(e,close_code,self.room_group_name))


    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        try:
            self.commands[data['command']](self, data)
        except Exception as e:
            logger.error('Exception={}, text_data={}. '.format(e,text_data))

    def send_chat_message(self, message):
        try: async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        except Exception as e:
            logger.error('Exception={}, message={}. while seding message into room={} '.format(e,message,self.room_group_name))

    def send_message(self, message):
        try:
            self.send(text_data=json.dumps(message))
        except Exception as e:
            logger.error('Exception={}, send message={} while sending message '.format(e,message))

    def chat_message(self, event):
        try:
            message = event['message']
            self.send(text_data=json.dumps(message))
        except Exception as e:
            logger.error('Exception={}, event={}. while loading chat message '.format(e,event))
