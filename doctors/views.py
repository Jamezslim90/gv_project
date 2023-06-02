from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import DoctorForm, OpeningHourForm, BankAccountForm, MeetingForm
from accounts.forms import UserProfileForm
from service.forms import ConsultationItemForm
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import UserProfile
from .models import  Doctor, OpeningHour, BankAccount, Meeting
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from service.models import ConsultationItem, Service
from clients.models import Appointment
from orders.models import Payment
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_doctor, check_role_customer
from django.template.defaultfilters import slugify
from datetime import datetime,time, date
import json
from .utils import createZoomMeeting
from .tasks import send_zoom_invitation, send_zoom_notification 
from accounts.utils import get_doctor
from django.http import HttpResponseForbidden
# Channels
from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
import json
from django.views.decorators.csrf import csrf_exempt



@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def dprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
   # doctor = get_object_or_404(Doctor, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
       #doctor_form = DoctorForm(request.POST, instance=doctor)
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
        fields = ['VCN_number', 'state_of_practice','induction_date', 'specialty']
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

@csrf_exempt
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


#  Bank CRUD VIEWS

@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def bank_info(request):
    doctor = get_doctor(request)
    banks = BankAccount.objects.filter(doctor=doctor)
    context = {
        'banks': banks,
    }
    return render(request, 'doctors/bank_list.html', context)

@csrf_exempt
@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def add_bank(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.doctor = get_doctor(request)
            form.save()
            messages.success(request, 'Bank added successfully!')
            return redirect('bank_info')
        else:
            print(form.errors)
    else:
        form = BankAccountForm()
        # modify this form
        #form.fields['category'].queryset = Service.objects.filter(owner=get_doctor(request))
    context = {
        'form': form,
    }
    return render(request, 'doctors/add_bank.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def edit_bank(request, pk=None):
    bank  = get_object_or_404(BankAccount, pk=pk)
    if request.method == 'POST':
        form = BankAccountForm(request.POST,  instance= bank)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.doctor = get_doctor(request)
            form.save()
            messages.success(request, 'Bank account updated successfully!')
            return redirect('bank_info')
        else:
            print(form.errors)

    else:
        form = BankAccountForm(instance=bank)
        # form.fields['category'].queryset = Category.objects.filter(vendor=get_doctor(request))
    context = {
        'form': form,
        'bank': bank,
    }
    return render(request, 'doctors/edit_bank.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def delete_bank(request, pk=None):
    bank = get_object_or_404(BankAccount, pk=pk)
    bank.delete()
    messages.success(request, 'Bank Account has been deleted successfully!')
    return redirect('bank_info')



@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(doctor=get_doctor(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'doctors/opening_hours.html', context)


def add_opening_hours(request):
    # handle the data and save them inside the database
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_offline = request.POST.get('is_offline')
            
            try:
                hour = OpeningHour.objects.create(doctor=get_doctor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_offline=is_offline)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_offline:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_offline': 'Offline'}
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+' already exists for this day!'}
                return JsonResponse(response)
        else:
            HttpResponse('Invalid request')


def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id': pk})


@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def meeting_info(request):
    
    doctor = get_doctor(request)
    meetings = Meeting.objects.filter(doctor=doctor)
    context = {
        'meetings': meetings,
    }
    return render(request, 'doctors/meeting_list.html', context)


def add_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.doctor = get_doctor(request)
            doctor_name = get_doctor(request).user.first_name + ' ' + get_doctor(request).user.last_name
            
            # Extract data from form
            meeting.timezone = 'Africa/Bangui'
            timezone = meeting.timezone
            email = request.POST.get('zoom_email')
            form_date= request.POST.get('date')
            form_time= request.POST.get('time')
            topic = request.POST.get('topic')
            duration = request.POST.get('duration')
            passcode= request.POST.get('passcode')
            customer_email = request.POST.get('customer_email')
            
                        
            start_time = form_date + 'T' + form_time
            # Create zoom meeeting
            response = createZoomMeeting(email,topic, start_time, duration, passcode, timezone)
            data = response
            # Convert the JSON response to a Python dictionary
            print(data)
            # Access a specific attribute in the response data
            id = data['id']
    
            meeting.zoom_id = id
            form.save()
            
            
         # SEND ZOOM INVITE EMAIL TO THE CUSTOMER
            mail_subject = 'Zoom meeting invitation- ' + topic + '.'
            mail_template = 'doctors/zoom_invitation_email.html'

            context = {
                'topic': data['topic'],
                'doctor': doctor_name,
                'to_email': customer_email,
                'start_time': data['start_time'],
                'zoom_meeting_id': data['id'],
                'duration': data['duration'],
                'join_url': data['join_url'],
                'password': data['password'],
            
            }
            send_zoom_invitation.delay(mail_subject, mail_template, context)
            

            #SEND ZOOM NOTIFICATION EMAIL TO THE DOCTOR
            mail_subject = 'Zoom meeting notification- ' + topic + '.'
            mail_template = 'doctors/zoom_notification_email.html'
            
            context = {
                'topic': data['topic'],
                'doctor': doctor_name,
                'to_email': email,
                'start_time': data['start_time'],
                'zoom_meeting_id': data['id'],
                'duration': data['duration'],
                'start_url': data['start_url'],
                'password': data['password'],
            
            }
            
            send_zoom_notification.delay(mail_subject, mail_template, context)
            
            messages.success(request, 'Meeting created successfully!')
            return redirect('meeting_info')
        else:
            print(form.errors)
    else:
        form = MeetingForm()
        context = {
        'form': form,
    }
    return render(request, 'doctors/add_meeting.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def doctor_appointment (request):
    
    doctor = get_doctor(request)
    appointments = Appointment.objects.filter(appointment_doctor=doctor)
    paginator = Paginator(appointments, 10)  # Show 25 contacts per page.
  
    
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
         
        'appointments': appointments, 
        'page_obj': page_obj  
    }
    return render(request, 'doctors/appointments_list.html', context)

   
    
@login_required(login_url='login')
@user_passes_test(check_role_doctor)     
def doctor_payment(request):
    
    doctor = get_doctor(request)
    payments = Payment.objects.filter(receiver=doctor)
    paginator = Paginator(payments, 10)  # Show 25 contacts per page.
  
    
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'payments': payments,
        'page_obj': page_obj
    }
    return render(request, 'doctors/payments_list.html', context)



# def order_detail(request, order_number):
#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))

#         context = {
#             'order': order,
#             'ordered_food': ordered_food,
#             'subtotal': order.get_total_by_vendor()['subtotal'],
#             'tax_data': order.get_total_by_vendor()['tax_dict'],
#             'grand_total': order.get_total_by_vendor()['grand_total'],
#         }
#     except:
#         return redirect('vendor')
#     return render(request, 'vendor/order_detail.html', context)


# def my_orders(request):
#     vendor = Vendor.objects.get(user=request.user)
#     orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')

#     context = {
#         'orders': orders,
#     }
#     return render(request, 'vendor/my_orders.html', context)




# from asgiref.sync import async_to_sync
# def test(request):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "notification_broadcast",
#         {
#             'type': 'send_notification',
#             'message': json.dumps("Notification")
#         }
#     )
#     return HttpResponse("Done")