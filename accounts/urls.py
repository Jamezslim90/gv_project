from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerDoctor/', views.registerDoctor, name='registerDoctor'),
    
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    
    path('managerdashboard/', views.mgrDashboard, name='managerDashboard'),
    path('customerDashboard/', views.custDashboard, name='customerDashboard'),
    path('doctorDashboard/', views.docDashboard, name='doctorDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
    path('doctor/', include('doctors.urls')),
    #path('customer/', include('customers.urls')),

]
