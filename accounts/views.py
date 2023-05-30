from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import message
from django.contrib import messages, auth
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from .forms import UserForm
from .models import User, UserProfile
from doctors.models import Doctor, Meeting
from django.template.defaultfilters import slugify
from doctors.forms import DoctorForm
from .utils import detectUser
from .tasks import send_verification_email
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
import json
from clients.models import Animal, Appointment
from vaccinations.models import Vaccination
from orders.models import Order, Payment
from django.db.models import Sum
from .utils import get_doctor
from .utils import get_customer
from .forms import UserForm, UserProfileForm
from notifications.models import DoctorNotification, CustomerNotification
from django.utils.dateparse import parse_datetime



# Restrict the vendor from accessing the customer page
def check_role_doctor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
# Restrict the customer from accessing the vendor page
def check_role_manager(user):
    if user.role == 3:
        return True
    else:
        raise PermissionDenied
        
    
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    
    elif request.method == "POST":
       form = UserForm(request.POST)
       if form.is_valid(): 
        # Create the user using the form
        # password = form.cleaned_data['password']
        # user = form.save(commit=False)
        # user.set_password(password)
        # user.role = User.CUSTOMER
        # user.save()

        # Create the user using create_user method
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.role = User.CUSTOMER
        user.save()
        
        # Send verification email
        mail_subject = 'Please activate your account'
        email_template = 'accounts/emails/account_verification_email.html'
        send_verification_email.delay(request, user, mail_subject, email_template)
        messages.success(request, "Successfully, we've sent a verification email!")
        return redirect('registerUser')
        
       else:
           print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/registerUser.html', context)


def registerDoctor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == "POST":
       print("precheck")
       form = UserForm(request.POST)
       d_form = DoctorForm(request.POST)
       if d_form.is_valid() and form.is_valid():
        print("checkform") 
            
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        print(first_name)
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.role = User.DOCTOR
        print(user)
        user.save()
        doctor = d_form.save(commit=False)
        doctor.user = user
        doctor.doctor_slug = slugify(username) +str(user.id)
        user_profile = UserProfile.objects.get(user=user)
        doctor.user_profile = user_profile
        doctor.vcn_number = d_form.cleaned_data['vcn_number']
        doctor.state_of_practice = d_form.cleaned_data['state_of_practice']
        #doctor.induction_date = d_form.cleaned_data['induction_date']
        #specialty= d_form.cleaned_data['specialty']
        #doctor.specialty.set(specialty) 
        print(doctor)
        doctor.save()
        
         # Send verification email
        mail_subject = 'Please activate your account'
        email_template = 'accounts/emails/account_verification_email.html'
        send_verification_email.delay(request, user, mail_subject, email_template)

        messages.success(request, "Successfully, we've sent a verification email!")
        return redirect('registerDoctor')
        
       else:
           print('invalid form')
           print(d_form.errors)
    else:
        form = UserForm() 
        d_form = DoctorForm()
    context = {
        'form': form,
        'd_form': d_form
    }
    
    return render(request, 'accounts/registerDoctor.html', context)


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    
    
def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
             # check if the user has previously logged in
            if user.last_login is not None:
                # add the last login time to the session data
                request.session['last_login'] = str(user.last_login)
                
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def LogoutView(request):
    
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('home')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    
    customer = get_customer(request)
    animal_count = Animal.objects.filter(owner=customer).count()
    user_payments = Payment.objects.filter(user=customer.user)
    appointment_count = Appointment.objects.filter(owner=customer).count()
    
    # session data
    
    customer_last_login = request.session.get('last_login') # String
    print(customer_last_login)
    
    parse_customer_last_login = parse_datetime(customer_last_login) # Converts to date Object
    print(parse_customer_last_login)
    
    latest_notifications = CustomerNotification.objects.filter(created_at__gt=datetime.date(parse_customer_last_login))
    
    print(latest_notifications)
    
    # aggregate the total amount
    total_payment = user_payments.aggregate(Sum('amount'))
    print(total_payment)
    total_sum_payment = total_payment['amount__sum']
    print(total_sum_payment)
    
    context = {
        
        'animal_count': animal_count,
        'total_sum_payment': total_sum_payment,
        'appointment_count': appointment_count,
        'room_name': "cusbroadcast",
        'latest_notifications':  latest_notifications
        
    }
    return render(request, 'accounts/customerDashboard.html' , context
    )

from asgiref.sync import async_to_sync
@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def docDashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    
    doctor_last_login = request.session.get('last_login') # String
   
    
    meeting_count = Meeting.objects.filter(doctor=doctor).count()
    doctor_revenue = Payment.objects.filter(receiver=doctor)
    appointment_count = Appointment.objects.filter(appointment_doctor=doctor).count()
    
    # aggregate the total amount
    total_revenue = doctor_revenue.aggregate(Sum('amount'))
    print(total_revenue)
    total_sum_revenue = total_revenue['amount__sum']
    print(total_sum_revenue)
    print(doctor_last_login)
    
    parse_doctor_last_login = parse_datetime(doctor_last_login) # Converts to date Object
    print(parse_doctor_last_login)
    
    latest_notifications = DoctorNotification.objects.filter(created_at__gt=datetime.date(parse_doctor_last_login))
    print(latest_notifications)
    
    
    context = {
        
        'meeting_count': meeting_count,
        'total_sum_revenue': total_sum_revenue,
        'appointment_count': appointment_count,
        'room_name': "docbroadcast",
        'latest_notifications': latest_notifications
            
    }
   
    return render(request, 'accounts/doctorDashboard.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_manager)
def mgrDashboard(request):
    
    # doctor = Doctor.objects.get(user=request.user)
    
    doctor_count = Doctor.objects.all().count()  
    client_count = User.objects.filter(role=2).count()
    meeting_count = Meeting.objects.all().count()
    revenue = Payment.objects.all()
    appointment_count = Appointment.objects.all().count()
    animal_count = Animal.objects.all().count()
    
    # aggregate the total amount
    
    total_revenue = revenue.aggregate(Sum('amount'))
    print(total_revenue)
    total_sum_revenue = total_revenue['amount__sum']
    print(total_sum_revenue)
    
    context = {
        
        'meeting_count': meeting_count,
        'total_sum_revenue': total_sum_revenue,
        'appointment_count': appointment_count,
        'animal_count': animal_count,
        'doctor_count': doctor_count,
        'client_count': client_count,
        
        
    }
    return render(request, 'accounts/managerDashboard.html', context )



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email.delay(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
@user_passes_test(check_role_manager)
def mprofile(request):
    
    """
    Display the user's profile.
    
    """
    profile = get_object_or_404(UserProfile, user=request.user)
   # doctor = get_object_or_404(Doctor, user=request.user)
    print(profile)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
       # doctor_form = DoctorForm(request.POST, instance=doctor)
        #doctor_form.induction_date = request.POST.get("induction_date")
        if profile_form.is_valid() : #and doctor_form.is_valid()
            profile_form.save()
           # doctor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            #print(doctor_form.errors)
    
    else:
        profile_form = UserProfileForm(instance=profile)
        #doctor_form = DoctorForm(instance=doctor)

    context = {
        'profile_form': profile_form,
        'profile': profile,
     
    }

    return render(request, 'manager/mprofile.html', context)