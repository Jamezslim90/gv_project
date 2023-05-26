from django.db import models
from accounts.models import User, UserProfile
from doctors.models import Doctor
from service.models import ConsultationItem
from datetime import date 
from dateutil.relativedelta import relativedelta

# from smart_selects.db_fields import ChainedForeignKey
# Create your models here.

class Category(models.Model):
    animal_category= models.CharField(max_length=15)
    
    def __str__(self):
        return self.animal_category
    
    class Meta:
        verbose_name_plural = 'Categories'

class AnimalType(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    animal_type = models.CharField(max_length=15)
    
    def __str__(self):
        return self.animal_type
    
class Symptom(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    
class Appointment(models.Model):
    
    owner = models.ForeignKey(UserProfile, related_name='clients_appointments', on_delete=models.CASCADE)
    appointment_doctor = models.ForeignKey(Doctor, related_name='doctors_appointments', on_delete=models.CASCADE)
    animal_category =models.ForeignKey(Category, on_delete=models.CASCADE)
    animal= models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom, blank=True)
    appointment_type = models.ForeignKey(ConsultationItem, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11)
    date = models.DateField( blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    optional_message = models.TextField()
    

    def __str__(self):
        return self.appointment_type.type.name
    
    class Meta:
        ordering = ['-date']
    
    
class Animal(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='clients_animals', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    animal_category =models.ForeignKey(Category, on_delete=models.CASCADE)
    animal= models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    animal_slug = models.SlugField(max_length=200, unique=True)
    profile_pic = models.ImageField(upload_to='animal_pics', blank=True, null=True)
    breed = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    weight = models.CharField(max_length=200, blank=True, null=True)
    last_vaccination_date = models.DateField(blank=True, null=True)
    next_vaccination_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    
    @property
    def age(self):
        if(self.dob != None):
            today = date.today()
            delta = relativedelta(today, self.dob)
            age_years = delta.years
            age_months = delta.months
            if age_years == 0 and age_months == 0:
                return "Less than a month old"
            elif age_years == 0:
                return f"{age_months} month{'s' if age_months > 1 else ''} old"
            else:
                return f"{age_years} year{'s' if age_years > 1 else ''} & {age_months} month{'s' if age_months > 1 else ''} old"
        else:
            return "N/A"

            


