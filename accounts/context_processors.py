from urllib.parse import uses_relative
from accounts.models import UserProfile, User
from doctors.models import Doctor
from django.conf import settings

def get_doctor(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except:
        doctor = None
    return dict(doctor=doctor)

def get_customer(request):
    try:
     customer = User.objects.get(user=request.user)
    except:
        customer = None
    return customer


def get_user_profile(request):
     try:
         user_profile = UserProfile.objects.get(user=request.user)
     except:
         user_profile = None
     return dict(user_profile=user_profile)



# def get_google_api(request):
#     return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


# def get_paypal_client_id(request):
#     return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}