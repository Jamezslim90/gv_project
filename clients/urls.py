from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [

 path('', AccountViews.custDashboard, name='customer'),
 path('profile/', views.cprofile, name='cprofile'),
 
 path('appointment_list/', views.appointment_list, name='appointment_list'),
 path('appointment_list/add/', views.add_appointment, name='add_appointment'),
 
 path('payment_list/', views.payment_list, name='payment_list'),
 path('vaccination_list/', views.vaccination_list, name='vaccination_list'),
 
 path('vaccine_done/', views.vaccine_done, name='vaccine_done'),
 
 path('animal_list/', views.animal_list, name='animal_list'),
 path('<slug:animal_slug>/', views.animal_detail, name='animal_detail'),
 
# Animal CRUD

path('animal_list/add/', views.add_animal, name='add_animal'),
path('animal_list/edit/<int:pk>/', views.edit_animal, name='edit_animal'),
path('animal_list/delete/<int:pk>/', views.delete_animal, name='delete_animal'),



# Bank CRUD

# path('bank_info/', views.bank_info, name='bank_info'),
# path('bank_info/add/', views.add_bank, name='add_bank'),
# path('bank_info/edit/<int:pk>/', views.edit_bank, name='edit_bank'),
# path('bank_info/delete/<int:pk>/', views.delete_bank, name='delete_bank'),


# path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
# path('my_orders/', views.my_orders, name='vendor_my_orders'),
   
]