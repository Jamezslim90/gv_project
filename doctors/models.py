#from enum import unique
from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
#from datetime import time, date, datetime
#from multiselectfield import MultiSelectField





class AnimalSpecialty (models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
         return self.name

class Doctor(models.Model):
    

    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vcn_number = models.CharField(max_length=7)
    state_of_practice = models.CharField(max_length=50)
    specialty = models.ManyToManyField(AnimalSpecialty, help_text='You can select multiple specialties')
    # specialty = MultiSelectField(max_length=50, choices=SPECIALTY_CHOICE, blank=True, null=True)
    induction_date = models.DateField(blank=True, null=True)
    doctor_slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
    def get_specialties(self):
        return "\n".join([p.specialty for p in self.specialty.all()])
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Doctor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = "Congratulations! Your licence has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your services on our platform."
                    send_notification(mail_subject, mail_template, context)
        return super(Doctor, self).save(*args, **kwargs)