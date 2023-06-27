# from django.http import HttpResponse, JsonResponse
# from django.db import IntegrityError
from django.core.paginator import Paginator
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserProfileForm
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.views import generic
from accounts.models import UserProfile, User
from .models import Animal, Appointment, Symptom, AnimalType
from vaccinations.models import Vaccination
from orders.models import Payment
from django.contrib import messages
from .forms import AnimalForm, AppointmentForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_customer
from django.template.defaultfilters import slugify
from orders.models import OrderedItem
from django.http import HttpResponseRedirect,JsonResponse
from datetime import datetime, timedelta
import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from accounts.utils import get_customer, send_appointment_email

# from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cprofile(request):
    
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
        'section': 'settings'
     
    }

    return render(request, 'clients/cprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def animal_list(request):
    
    """
    List all animals for the current user.
    
    """
    customer = get_customer(request)
    animals = Animal.objects.filter(owner=customer)
    paginator = Paginator(animals, 10)  # Show 25 contacts per page.
  
    
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'animals': animals,
        'page_obj': page_obj,
        'section': 'animals'
    }
    return render(request, 'clients/animal_list.html', context)


# Animal Views

def animal_detail(request, animal_slug):
    """This view displays the details of an animal.

    Args:
        request (object): The request object.
        animal_slug (string): The slug of the animal to display.

    Returns:
        object: The rendered animal detail template.
    """
    animal = get_object_or_404(Animal, animal_slug=animal_slug)
    completed_vaccination_count= Vaccination.objects.filter(animal=animal, completed=True).count()
    total_vaccination_count= Vaccination.objects.all().filter(animal=animal).count()
        
    context = {
        'animal': animal,
        'completed_vaccination_count': completed_vaccination_count,
        'total_vaccination_count': total_vaccination_count,
    }
    return render(request, 'clients/animal_detail.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def add_animal(request):
   
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']  
            animal= form.save(commit=False)
            animal.owner = get_customer(request)
            animal.animal_slug = slugify(name)+'-'+str(animal.id)
            form.save()
            messages.success(request, 'Animal added successfully!')
            return redirect('animal_list')
        else:
            print(form.errors)
    else:
        form = AnimalForm()

    context = {
        'form': form,
    }
    return render(request, 'clients/add_animal.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def edit_animal(request, pk=None):
    animal= get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST,  instance= animal)
        if form.is_valid():
            name = form.cleaned_data['name']
            animal = form.save(commit=False)
            animal.owner = get_customer(request)
            animal.animal_slug = slugify(name)
            form.save()
            messages.success(request, 'Animal info updated successfully!')
            return redirect('animal_list')
        else:
            print(form.errors)

    else:
        form = AnimalForm(instance=animal)
       
    context = {
        'form': form,
        'animal': animal,
    }
    return render(request, 'clients/edit_animal.html', context)
  
    
def delete_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    animal.delete()
    messages.success(request, 'Animal deleted.')
    return redirect('animal_list')




@login_required(login_url='login')
@user_passes_test(check_role_customer)
def vaccine_done(request):
    
    """_summary_: This view updates the vaccination status to completed and sends a reminder email to the user.
      
      Args:
        request (object): The request object.
        
      Returns:
        object: The rendered animal detail template.  
    """
    # animal = get_object_or_404(Animal, animal_slug=animal_slug)
    if request.method == 'POST':
        date = request.POST.get("date")
        print(date)
        vaccination_id =                    request.POST.get("vaccination-id")
        vaccination =                       Vaccination.objects.get(id=vaccination_id)
        vaccination.completed =             True
        vaccination.date_administered =     date
        
        # TODO
        # Update the Animal Model with the last vaccination date
        animal_id = request.POST.get("animal-id")
        animal= Animal.objects.get(id=animal_id)
        animal.last_vaccination_date = date
        
        # Calculate the next vaccination date
        expiration_period =   request.POST.get("expiration-date") # get exp date from the form
        date_object =   datetime.strptime(date, '%Y-%m-%d').date() #convert datestring to date obj 
        animal.next_vaccination_date =  date_object + timedelta(days=int(expiration_period))
        print(animal.next_vaccination_date)
        vaccination.save()    #save vaccination
        animal.save()         #save animal
        
        mail_subject =      'Vaccination Reminder'
        mail_template =     'clients/vaccination_pre_exp.html'
        mail_template2 = 'clients/vaccination_on_exp.html'
        
        # Get the customer object
        
        customer = get_customer(request)
        email = str(customer.user.email)
    
        #convert next_vaccination_date to string
        
        next_vaccination_date_string = animal.next_vaccination_date.strftime("%Y-%m-%d")
        animal_name = animal.name
        animal_owner = animal.owner.user.first_name
        next_vaccination_date = next_vaccination_date_string
        last_vaccination_date = animal.last_vaccination_date
        
        # Append animal data into the  context object below:
        context = {

            'animal_name': animal_name,
            'animal_owner': animal_owner,
            'to_email': email,
            'next_vaccination_date': next_vaccination_date,
            'last_vaccination_date': last_vaccination_date,
                  
        }
        
        # Time to call celery-beat to shedule a task 
        # (next vaccination email remainder) for celery at periodic intervals.
        
        # Create a dynamic schedule with the expiration period 
        
         #Now, get the interval schedule
        days_before_expiration = 3          # 3 days before expiration
        three_days_to_go_date  = animal.next_vaccination_date -  timedelta(days=days_before_expiration)
        
        #Split the date into year, month, day, hour, minute, second
        
        #year = three_days_to_go_date.year
        month = three_days_to_go_date.month
        day = three_days_to_go_date.day
         
        schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=30,
        hour=11,
        day_of_month=day,
        month_of_year=month, 
 )
        
        #Get One day to go date
        day_before_expiration = 1 
        one_day_to_go_date  = animal.next_vaccination_date -  timedelta(days=day_before_expiration)
        
        #Split the date into year, month, day, hour, minute, second
        
        #year = one_day_to_go_date.year
        month = one_day_to_go_date.month
        day = one_day_to_go_date.day
        
        schedule2, _ = CrontabSchedule.objects.get_or_create(
        minute=30,
        hour=11,
        day_of_month=day,
        month_of_year=month,
 )
          
          
        #Get the day of the vaccination date
        vaccination_date  = animal.next_vaccination_date 
        
        #Split the date into year, month, day, hour, minute, second
        
        #year = one_day_to_go_date.year
        month = vaccination_date.month
        day = vaccination_date.day
        
        schedule3, _ = CrontabSchedule.objects.get_or_create(
        minute=30,
        hour=11,
        day_of_month=day,
        month_of_year=month,
 )

        
        string_vaccination_id = str(vaccination_id)
        #OK!, then create the actual shedule
         #First task   
        task1= PeriodicTask.objects.create(
        crontab=schedule,                                            # we created this above.
        name=' 3 days to go email' + string_vaccination_id,          # simply describes this periodic task.
        task='clients.tasks.send_vaccination_pre_exp',               # name of task.
        args=json.dumps((mail_subject, mail_template, context)),
        one_off=True,
        )
        
          #Second task
        task2 = PeriodicTask.objects.create(
        interval=schedule2,                                   # we created this above.
        name='1 day to go email' + string_vaccination_id,    # simply describes this periodic task.
        task='clients.tasks.send_vaccination_pre_exp',             # name of task.
        args=json.dumps((mail_subject, mail_template, context)),
        one_off=True,
        
        )
     
        #Third task
        task3= PeriodicTask.objects.create(
        interval=schedule3,                                      # we created this above.
        name='Send Email onday' + string_vaccination_id,          # simply describes this periodic task.
        task='clients.tasks.send_vaccination_on_exp',             # name of task.
        args=json.dumps((mail_subject, mail_template2, context)),
        one_off=True,
        
        )
        
        
           
        # Send a success message to the user
        messages.success(request, 'Vaccination updated successfully!')
        return redirect('animal_detail', animal_slug=vaccination.animal.animal_slug)
    else:
        messages.warning(request, 'Vaccination update failed!')  # Send a failure message to the user
        return redirect('animal_list')



# Appointment Views

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def appointment_list(request):
    customer = get_customer(request)
    appointments = Appointment.objects.filter(owner=customer)
    paginator = Paginator(appointments, 10)  # Show 25 contacts per page.
  
    
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        
        'appointments': appointments,
        "page_obj":  page_obj
        
    }
    return render(request, 'clients/appointments_list.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def add_appointment(request):
    
    ordered_item = OrderedItem.objects.filter(user=request.user).last()
    if request.method == 'POST':
         form = AppointmentForm(request.POST)
         if form.is_valid(): 
            appointment= form.save(commit=False)
            appointment.owner = get_customer(request).user.userprofile
            appointment.email = get_customer(request).user.email
            appointment.phone = get_customer(request).phone_number
            appointment.appointment_type = ordered_item.item
            appointment.appointment_doctor = ordered_item.item.owner
            
            # SEND APPOINTMENT EMAIL TO DOCTOR
            # TODO
            mail_subject = 'New Appointment'
            mail_template = 'doctors/appointment_email.html'
            email = ordered_item.item.owner.user.email
            doctor = ordered_item.item.owner
            user = get_customer(request).user
            
            
            context = {
                
                 'to_email': email,
                 'doctor': doctor,
                 'user': user,
            }
            send_appointment_email(mail_subject, mail_template, context)
            
            form.save()
            messages.success(request, 'Appointment successful!')
            return redirect('myAccount')
         else:
            print(form.errors)
    else:
        form = AppointmentForm()

    context = {
        'form': form,
    }
    return render(request, 'clients/add_appointment.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def payment_list(request):
    customer = get_customer(request)
    payments = Payment.objects.filter(user=customer.user)
    paginator = Paginator(payments, 10)  # Show 25 contacts per page.
   
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        
        'payments': payments,
        'page_obj': page_obj,
        'section': 'payments',
    }
    return render(request, 'clients/payments_list.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def vaccination_list(request):
    customer = get_customer(request)
    animals = Animal.objects.filter(owner=customer)
    animal_vaccinations = []
    animal_vaccine = []
    for animal in animals:
        animal_vaccinations.append(animal.vaccinations.all())
    
    for vaccinations in animal_vaccinations:
        for vaccine in vaccinations:
            animal_vaccine.append(vaccine)
    
    paginator = Paginator(animal_vaccine, 4)  # Show 25 contacts per page.
  
    
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'animal_vaccine': animal_vaccine,
        'page_obj': page_obj,
        'section': 'vaccinations'
    }
    return render(request, 'clients/vaccinations_list.html', context)
