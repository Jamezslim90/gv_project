from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [

 path('', AccountViews.docDashboard, name='doctor'),
 path('profile/', views.dprofile, name='dprofile'),
 path('<int:pk>/edit_doctor_info_page/', views.EditDoctorInfoPage.as_view(), name='edit_doctor_info_page'),
 
 path('consultation_item/', views.consultation_item, name='consultation_item'),
 
 
 # item CRUD
 
path('consultation_item/item/add/', views.add_item, name='add_item'),
path('consultation_item/item/edit/<int:pk>/', views.edit_item, name='edit_item'),
path('consultation_item/item/delete/<int:pk>/', views.delete_item, name='delete_item'),

    
]