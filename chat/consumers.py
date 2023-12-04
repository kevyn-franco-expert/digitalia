# chat/consumers.py

import json
import time

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Conversation


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.conversation_id = None
        self.user = None
        self.last_message_timestamp = {}

    async def connect(self):
        self.user = self.scope["user"]
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        print('user:', self.user)
        print('conversation_id:', self.conversation_id)
        print('room_group_name:', self.room_group_name)

        # Check if conversation exists and user is a participant
        if not await self.is_participant(self.user, self.conversation_id):
            await self.close()
            return

        print('Is participant')
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        messages = await self.get_conversation_messages(self.conversation_id)
        for message in messages:
            await self.send(text_data=json.dumps({
                'user': message['user__username'],
                'message': message['text'],
                'timestamp': f"[{message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}]"  # Format timestamp
            }))

    async def receive(self, text_data):
        current_timestamp = time.time()
        user_id = self.scope["user"].id

        if user_id in self.last_message_timestamp:
            elapsed_time = current_timestamp - self.last_message_timestamp[user_id]
            if elapsed_time < 1:
                await self.send(text_data=json.dumps({'error': 'Throttled'}))
                return

        self.last_message_timestamp[user_id] = current_timestamp

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_message(self.user, self.conversation_id, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'conversation_id': self.conversation_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user': user,
            'message': message,
            'conversation_id': self.conversation_id,
        }))

    @database_sync_to_async
    def save_message(self, user, conversation_id, message_text):
        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.create(user=user, conversation=conversation, text=message_text)
        message.save()

    @database_sync_to_async
    def is_participant(self, user, conversation_id):
        conversation, created = Conversation.objects.get_or_create(id=conversation_id)
        if user not in conversation.participants.all():
            conversation.participants.add(user)
            conversation.save()
        return True

    @database_sync_to_async
    def get_conversation_messages(self, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id)
        return list(conversation.messages.order_by('timestamp').values('user__username', 'text', 'timestamp')[
                    :50])  # Fetch last 50 messages
