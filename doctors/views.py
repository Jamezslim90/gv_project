from django.shortcuts import render, get_object_or_404, redirect
from .forms import DoctorForm #OpeningHourForm
from accounts.forms import UserProfileForm
from service.forms import ConsultationItemForm
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import UserProfile
from .models import  Doctor #OpeningHour
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from service.models import ConsultationItem, Service

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_doctor
from django.template.defaultfilters import slugify



def get_doctor(request):
    doctor = Doctor.objects.get(user=request.user)
    return doctor



@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def dprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
   # doctor = get_object_or_404(Doctor, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
       # doctor_form = DoctorForm(request.POST, instance=doctor)
        #doctor_form.induction_date = request.POST.get("induction_date")
        if profile_form.is_valid() : #and doctor_form.is_valid()
            profile_form.save()
           # doctor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('dprofile')
        else:
            print(profile_form.errors)
            #print(doctor_form.errors)
    
    else:
        profile_form = UserProfileForm(instance=profile)
        #doctor_form = DoctorForm(instance=doctor)

    context = {
        'profile_form': profile_form,
        #'doctor_form': doctor_form,
        'profile': profile,
        #'doctor': doctor,
    }

    return render(request, 'doctors/dprofile.html', context)


class EditDoctorInfoPage(SuccessMessageMixin, generic.UpdateView):
        model = Doctor
        
        template_name = 'doctors/doctor_info_page.html'
        fields = ['vcn_number', 'state_of_practice','induction_date', 'specialty']
        success_url = reverse_lazy('doctorDashboard')
        suceess_message = "info updated successful"


    
@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def consultation_item(request):
    doctor = get_doctor(request)
    consultation_item = ConsultationItem.objects.filter(owner=doctor).order_by('created_at')
    context = {
        'consultation_item': consultation_item,
    }
    return render(request, 'doctors/consultation_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def add_item(request):
    if request.method == 'POST':
        form = ConsultationItemForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            item = form.save(commit=False)
            item.owner = get_doctor(request)
            item.slug = slugify(description)
            form.save()
            messages.success(request, 'Service added successfully!')
            return redirect('consultation_item')
        else:
            print(form.errors)
    else:
        form = ConsultationItemForm()
        # modify this form
        #form.fields['category'].queryset = Service.objects.filter(owner=get_doctor(request))
    context = {
        'form': form,
    }
    return render(request, 'doctors/add_item.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def edit_item(request, pk=None):
    item  = get_object_or_404(ConsultationItem, pk=pk)
    if request.method == 'POST':
        form = ConsultationItemForm(request.POST,  instance= item)
        if form.is_valid():
            description = form.cleaned_data['description']
            item = form.save(commit=False)
            item.doctor = get_doctor(request)
            item.slug = slugify(description)
            form.save()
            messages.success(request, 'Service Item updated successfully!')
            return redirect('consultation_item')
        else:
            print(form.errors)

    else:
        form = ConsultationItemForm(instance=item)
        # form.fields['category'].queryset = Category.objects.filter(vendor=get_doctor(request))
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'doctors/edit_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def delete_item(request, pk=None):
    item = get_object_or_404(ConsultationItem, pk=pk)
    item.delete()
    messages.success(request, 'Service Item has been deleted successfully!')
    return redirect('consultation_item')
