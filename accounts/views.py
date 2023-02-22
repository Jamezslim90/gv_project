from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import message
from django.contrib import messages, auth
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User, UserProfile
from doctors.models import Doctor
from doctors.forms import DoctorForm




def registerUser(request):
    if request.method == "POST":
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
        messages.success(request, 'Account sucessfully registered!')
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
    if request.method == "POST":
       form = UserForm(request.POST)
       d_form = DoctorForm(request.POST)
       if form.is_valid() and d_form.is_valid():
           
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
        user.role = User.DOCTOR
        user.save()
        doctor = d_form.save(commit=False)
        doctor.user = user
        user_profile = UserProfile.objects.get(user=user)
        doctor.user_profile = user_profile
        doctor.vcn_number = d_form.cleaned_data['vcn_number']
        doctor.state_of_practice = d_form.cleaned_data['state_of_practice']
        doctor.save()
        
        messages.success(request, 'Account sucessfully registered! Please wait for approval.')
        return redirect('registerDoctor')
        
       else:
           print(form.errors)
    else:
        form = UserForm()
        d_form = DoctorForm()
    context = {
        'form': form,
        'd_form': d_form
    }
    
    return render(request, 'accounts/registerDoctor.html', context)