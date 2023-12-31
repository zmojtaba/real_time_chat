import base64
import json
import secrets
from datetime import datetime
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.core.files.base import ContentFile
from channels.db import database_sync_to_async

from django.db.models import Q
from asgiref.sync import sync_to_async
from .models import Message, Conversation
from .api.serializer import MessageSerializer
from channels.layers import get_channel_layer
import getpass

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        current_user = await self.get_user(username = 'kaka@gmail.com' )
        other_user = await self.get_user(username = self.scope['url_route']['kwargs']['username'] )
        self.conversation = Conversation.objects.filter(Q(starter=current_user, receiver=other_user)|Q(starter=current_user, receiver=other_user))

        print('________________consumer_____________', other_user, current_user)

        self.room_name = (
            f"{current_user.id}_{other_user.id}"
            if current_user.id > other_user.id
            else f"{other_user.id}_{current_user.id}"
        )
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(close_code)


    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender =            await self.get_user(data['senderUsername'])
        receiver =          await self.get_user(data['receiverUsername'])

        # await self.save_message(sender, receiver, message)

        messages = await self.get_messages()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'senderUsername': sender.username,
                # 'messages': messages,
            },
        )       
        print("________________________________receiver is finished")

    async def chat_message(self, event):
        print("_____________________________chat message_________________________", event)
        message = event['message']
        username = event['senderUsername']
        # messages = event['messages']

        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'senderUsername': username,
                    # 'messages': messages,
                }
            )
        )

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.filter(username=username).first()

    @database_sync_to_async
    def get_conversation(self, starter, receiver):
        return (Conversation.objects.select_related().filter(Q(starter=starter, receiver=receiver)|Q(starter=receiver, receiver=starter)).first())


    @database_sync_to_async
    def get_messages(self):
        messages = self.conversation.first().message_conversation.all()
        messages = MessageSerializer(messages, many=True)
        return messages


    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        Message.objects.create(sender=sender, text=message, conversation=self.conversation.first())