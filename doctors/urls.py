from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [

 path('', AccountViews.docDashboard, name='doctor'),
 path('profile/', views.dprofile, name='dprofile'),
 path('<int:pk>/edit_doctor_info_page/', views.EditDoctorInfoPage.as_view(), name='edit_doctor_info_page'),
 
 path('consultation_item/', views.consultation_item, name='consultation_item'),
 
 
 # Item CRUD
 
path('consultation_item/item/add/', views.add_item, name='add_item'),
path('consultation_item/item/edit/<int:pk>/', views.edit_item, name='edit_item'),
path('consultation_item/item/delete/<int:pk>/', views.delete_item, name='delete_item'),

path('bank_info/', views.bank_info, name='bank_info'),

# Bank CRUD
 
path('bank_info/add/', views.add_bank, name='add_bank'),
path('bank_info/edit/<int:pk>/', views.edit_bank, name='edit_bank'),
path('bank_info/delete/<int:pk>/', views.delete_bank, name='delete_bank'),

 # Opening Hour CRUD
path('opening-hours/', views.opening_hours, name='opening_hours'),
path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

# path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
# path('my_orders/', views.my_orders, name='vendor_my_orders'),
   
]