#from enum import unique
from django.db import models
from accounts.models import User, UserProfile
from accounts.tasks import send_notification
from datetime import time, date, datetime
#from multiselectfield import MultiSelectField
from dateutil.relativedelta import relativedelta


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
        return self.user.first_name + " " + self.user.last_name
    
    def get_specialties(self):
        return "\n".join([p.specialty for p in self.specialty.all()])
    
    @property
    def experience(self):
        if(self.induction_date != None):
            today = date.today()
            delta = relativedelta(today, self.induction_date)
            exp_years = delta.years
            exp_months = delta.months
            if exp_years == 0 and exp_months == 0:
                return "Less than a month "
            elif exp_years == 0:
                return f"{exp_months} mo{'s' if exp_months > 1 else ''} "
            else:
                return f"{exp_years} yr{'s' if exp_years > 1 else ''} & {exp_months} mo{'s' if exp_months > 1 else ''} "
        else:
            return "N/A"

    
    def is_online(self):
        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(doctor=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_online = None
        for i in current_opening_hours:
            if not i.is_offline:
                start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_online = True
                    break
                else:
                    is_online = False
        return is_online
    
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
                    send_notification.delay(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your services on our platform."
                    send_notification.delay(mail_subject, mail_template, context)
        return super(Doctor, self).save(*args, **kwargs)
    
    
    
DAYS = [
    (1, ("Mon")),
    (2, ("Tue")),
    (3, ("Wed")),
    (4, ("Thu")),
    (5, ("Fri")),
    (6, ("Sat")),
    (7, ("Sun")),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_offline = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('doctor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()
    
    


class BankAccount(models.Model):
    BANK_CHOICES = (
        ('Access', 'Access'),
        ('GTBank', 'GTBank'),
        ('9PSB', '9PSB'),
        ('OPAY', 'OPAY'),
        ('Kuda', 'Kuda'),
        ('First', 'First'),
        ('FCMB', 'FCMB'),
        ('UBA', 'UBA'),
        ('Moniepoint', 'Moniepoint'),
        ('Palmpay', 'Palmpay'),
        ('Wema', 'Wema'),
        ('Fidelity', 'Fidelity'),
        ('Jaiz', 'Jaiz'),
        ('Keystone', 'Keystone'),
        ('Polaris', 'Polaris'),
        ('Stanbic-ibtc', 'Stanbic-ibtc'),
        ('Sterling', 'Sterling'),
        ('Taj', 'Taj'),
        ('Union', 'Union'),
        ('Unity', 'Unity'),
        ('Zenith', 'Zenith'),
        
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
    account_number = models.CharField(max_length=10)
    account_name = models.CharField(max_length=50)
  

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    
    
class Meeting(models.Model):
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    passcode= models.CharField(max_length=10)
    customer_email= models.EmailField()
    zoom_email= models.EmailField(help_text="Your zoom email address")
    duration= models.PositiveSmallIntegerField(default=30, blank=True)
    timezone= models.CharField(max_length=50, blank=True)
    zoom_id= models.CharField(max_length=50, blank=True)
        
        
    def __str__(self):
        return self.topic
    
    class Meta:
        ordering = ('-date',)
            
            
    
    