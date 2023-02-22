#from enum import unique
from django.db import models
from accounts.models import User, UserProfile
#from accounts.utils import send_notification
#from datetime import time, date, datetime
from multiselectfield import MultiSelectField




class AnimalSpecialty (models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
         return self.name

class Doctor(models.Model):
    
    SPECIALTY_CHOICE = (
        ('cat', 'Cat'),
        ('cattle', 'Cattle'),
        ('dog', 'Dog'),
        ('goat', 'Goat'),
        ('horse', 'Horse'),
        ('poultry', 'Poultry'),
        ('sheep', 'Sheep'),
    )
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vcn_number = models.CharField(max_length=7)
    state_of_practice = models.CharField(max_length=50)
    # specialty = models.ManyToManyField(AnimalSpecialty, help_text='You can select multiple specialties')
    specialty = MultiSelectField(max_length=50, choices=SPECIALTY_CHOICE, blank=True, null=True)
    #vendor_slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name