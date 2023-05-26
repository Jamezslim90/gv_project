from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth.models import User as Users,AnonymousUser
import json
from django.utils import timezone
from .models import Chat, ChatRoom
from channels.exceptions import StopConsumer

     
@database_sync_to_async
def createChat(content, room, user):
    chat = Chat.objects.create(content=content, room=room, user=user)
    return chat

class ChatAppConsumer(AsyncWebsocketConsumer):
    
    
    async def websocket_connect(self,event):
        print('connected',event)
        print(self.scope['user'].id)
        
        self.user = self.scope['user']
        
        # Channel layer
        self.id = self.scope['url_route']['kwargs']['doctor_slug']
        self.room_group_name = f'chat_{self.id}'
        
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # accept connection
        await self.accept()
       
    async def websocket_receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data['text'])
        message = text_data_json['message']
        now = timezone.now()
        content = message
        user = self.scope['user']
        # Find room Object
        room = await database_sync_to_async(ChatRoom.objects.get)(name=self.id)
        
        # Create new chat object in the database 
        myChat = await createChat(content, room, user)
        await database_sync_to_async(myChat.save)()
        
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )
    
         
    async def websocket_disconnect(self,event):
         # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('disconnect',event)
        raise StopConsumer()
        
     
        
    async def chat_message(self,event):
          # send message to WebSocket
        await self.send(text_data=json.dumps(event))

        print('Fired from chat_message')
        print(event)
        








