import json
from asgiref.sync import async_to_sync
from chat.models import Message
from core.models import Student, Collaboration
from django.shortcuts import get_object_or_404
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from rest_framework.exceptions import PermissionDenied


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        collaboration_id = self.scope['url_route']['kwargs']['collaboration_id']
        collaboration = get_object_or_404(Collaboration, id=collaboration_id)
        student = self.scope['student']
        if student != collaboration.applicant and student !=collaboration.collaborator:
            raise PermissionDenied('You don\'t have permission to perform this action')
        chat_room = f'chat_{collaboration_id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        message = event.get('text', None)
        if message is not None:
            collaboration_id = self.scope['url_route']['kwargs']['collaboration_id']
            collaboration = get_object_or_404(Collaboration, id=collaboration_id)
            student = self.scope['student']
            message_object = Message.objects.create(text=message, sender=student, collaboration=collaboration, read=False)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': str({'id': message_object.id, 'text': message, 'sender': message_object.sender.user.id}),
                    
                }
            )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })



