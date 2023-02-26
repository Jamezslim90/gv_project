from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [

 path('', AccountViews.docDashboard, name='doctor'),
 path('profile/', views.dprofile, name='dprofile'),
 path('<int:pk>/edit_doctor_info_page/', views.EditDoctorInfoPage.as_view(), name='edit_doctor_info_page'),
    
]