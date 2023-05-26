# chat/routing.py
from django.urls import re_path

from notifications.consumers import CustomerNotificationConsumer, DoctorNotificationConsumer

from chatapp.consumers import ChatAppConsumer

websocket_urlpatterns = [ 
    
    re_path(r"ws/notification/(?P<room_name>\w+)/$", CustomerNotificationConsumer.as_asgi()),
    re_path(r"ws/notification/(?P<room_name>\w+)/$", DoctorNotificationConsumer.as_asgi()),
    re_path(r'ws/chat/room/(?P<doctor_slug>\w+)/$', ChatAppConsumer.as_asgi()),
  
    
]


 