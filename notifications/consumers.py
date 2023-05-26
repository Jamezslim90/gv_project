from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth.models import User as Users,AnonymousUser
import json
from django.utils import timezone
from channels.exceptions import StopConsumer


@database_sync_to_async
def get_user(user_id):
    try:
        return Users.objects.get(id=user_id)
    except:
        return AnonymousUser()
    
# @database_sync_to_async
# def create_notification(receiver, typeof="task_created",status="unread"):
#     notification_to_create= Notifications.objects.create(user_revoker=receiver,type_of_notification=typeof)
#     print('I am here to help')
#     return (notification_to_create.user_revoker.username,notification_to_create.type_of_notification)


class CustomerNotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        print('connected',event)
        print(self.scope['user'].id)
        
        await self.accept()
       
        # Channel layer
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name
      
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        self.send({
            "type":"websocket.send",
            "text":"room made"
        })
       
    async def websocket_receive(self,event):
        
        print(event)
        
    async def websocket_disconnect(self,event):
        raise StopConsumer()
        print('disconnect',event)
        
    async def send_notification(self,event):
        await self.send(json.dumps({
            "type":"websocket.send",
            "data":event
        }))
        print('Fired from send_notification')
        print(event)
        
        



class DoctorNotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        print('connected',event)
        print(self.scope['user'].id)
        
        await self.accept()
       
        # Channel layer
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name
      
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        self.send({
            "type":"websocket.send",
            "text":"room made"
        })
       
    async def websocket_receive(self,event):
        
        print(event)
        
    async def websocket_disconnect(self,event):
        raise StopConsumer()
        print('disconnect',event)
        
    async def send_notification(self,event):
        await self.send(json.dumps({
            "type":"websocket.send",
            "data":event
        }))
        print('Fired from send_notification')
        print(event)
        
        
    