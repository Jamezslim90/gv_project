from django.urls import path
from . import views

urlpatterns = [
    path('', views.laboratory, name='laboratory'),
    path('<int:pk>/', views.laboratory_detail, name='laboratory_detail'),
    
]