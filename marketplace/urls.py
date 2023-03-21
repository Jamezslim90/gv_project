from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    
    path('<slug:doctor_slug>/', views.doctor_detail, name='doctor_detail'),

     # ADD TO CART
     path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
     # DECREASE CART
    path('decrease_cart/<int:item_id>/', views.decrease_cart, name='decrease_cart'),
     # DELETE CART ITEM
     path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
    
]