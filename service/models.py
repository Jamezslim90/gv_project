from django.db import models
from doctors.models import Doctor


class Service(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
    def __str__(self):
        return self.name



class Consultation(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.name
 
 
class Fee (models.Model):
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
         return str(self.fee)



class ConsultationItem(models.Model):
    owner= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    category = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='consultation_items')
    type = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    description = models.TextField(max_length=250, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.type)
