from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import message
from django.contrib import messages, auth
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from .forms import UserForm
from .models import User, UserProfile
from doctors.models import Doctor
from django.template.defaultfilters import slugify
from doctors.forms import DoctorForm
from .utils import detectUser, send_verification_email
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test




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
        send_verification_email(request, user, mail_subject, email_template)
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
        print(first_name)
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.role = User.DOCTOR
        print(user)
        user.save()
        doctor = d_form.save(commit=False)
        doctor.user = user
        doctor.doctor_slug = slugify(username)+'-'+str(user.id)
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
        send_verification_email(request, user, mail_subject, email_template)

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
    return render(request, 'accounts/customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def docDashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'accounts/doctorDashboard.html')



@login_required(login_url='login')
@user_passes_test(check_role_manager)
def mgrDashboard(request):
    return render(request, 'accounts/managerDashboard.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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