from django.db import models
from accounts.models import User
# Create your models here.



class ChatRoom(models.Model):
    name = models.CharField(max_length=1000)
 
    def __str__ (self):
        return self.name
 
class Chat(models.Model):
    
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)


    def __str__ (self):
        return self.content

    class meta:
        ordering = ['-timestamp']