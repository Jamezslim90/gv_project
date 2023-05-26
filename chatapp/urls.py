from django.urls import path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    
# Chat 
path('room/<slug:doctor_slug>/', views.chatRoom, name='chatRoom'),

]