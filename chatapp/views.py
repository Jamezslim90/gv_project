from django.shortcuts import render
from doctors.models import Doctor
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Chat, ChatRoom
from accounts.views import check_role_customer, check_role_doctor
# Create your views here.



@login_required(login_url='login') 
def chatRoom(request, doctor_slug):

   
    doctor = get_object_or_404(Doctor, doctor_slug=doctor_slug)
            
    room = ChatRoom.objects.filter(name=doctor_slug).first()
    chats= []
    if room:
            chats = Chat.objects.filter(room=room).order_by('timestamp')[:10]
        
    else: 
            room = ChatRoom.objects.create(name=doctor_slug)
        
  
   
    context = {
        
        'doctor': doctor,
        'doctor_slug': doctor.doctor_slug,
        'chats': chats
        
    }
    return render(request, 'chat/room.html', context)
