from django.db import models
from clients.models import  AnimalType



class Service (models.Model):
    
    type= models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Services'


class Laboratory(models.Model):
    
    # This is a Model for storing  Laboratories
    # Todo: Add a brand field to this model

    name =              models.CharField(max_length=200)
    animal_type=        models.ManyToManyField(AnimalType, blank=True)
    description =       models.TextField(blank=True, null=True)
    services=        models.ManyToManyField(Service, help_text='Select a feature for this project')
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Laboratories'


class Branch(models.Model):
    # A model for storing branches of a laboratory
    lab =                models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='branches',)
    phone_number =      models.CharField(max_length=11)
    email=              models.EmailField(max_length=50, blank=True, null=True)
    address=            models.CharField(max_length=20, blank=True, null=True)
    city=               models.CharField(max_length=20, blank=True, null=True)
    state=              models.CharField(max_length=20, blank=True, null=True)
   
    
    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = 'Branches'


     