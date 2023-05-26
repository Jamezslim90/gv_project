from django.contrib import admin
from .models import Chat, ChatRoom


class ChatAdmin(admin.ModelAdmin):
    list_display = ('room','user','content','timestamp',)
    
    
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)