from django.shortcuts import render, get_object_or_404, redirect
from .forms import DoctorForm #OpeningHourForm
from accounts.forms import UserProfileForm

from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import UserProfile
from .models import  Doctor #OpeningHour
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin


from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_doctor

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

    
