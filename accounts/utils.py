from .models import UserProfile
from doctors.models import Doctor

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'doctorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == 3:
        redirectUrl = 'managerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl



def get_customer(request):
    
    customer = UserProfile.objects.get(user=request.user)
    return customer


# def get_manager(request):
    
#     manager = UserProfile.objects.get(user=request.user)
#     return manager


def get_doctor(request):
    doctor = Doctor.objects.get(user=request.user)
    return doctor