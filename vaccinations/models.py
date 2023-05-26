from django.db import models
from accounts.models import User
from clients.models import Animal, AnimalType, Category, Symptom



class Disease(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    symptoms=models.ManyToManyField(Symptom, blank=True)
    animal_type=models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    
    def __str__(self): 
        return self.name

class Vaccine(models.Model):
    
    name = models.CharField(max_length=200)
    animal_type=models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    dosage=models.CharField(max_length=20, blank=True, null=True)
    desease=models.ManyToManyField(Disease, blank=True)
    age_of_vaccination=models.IntegerField()
    expiration_period=models.IntegerField()
    
    def __str__(self):
        return self.name

class Vaccination(models.Model):
    
    vaccine_name=models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    animal=models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='vaccinations',)
    completed=models.BooleanField(default=False)
    date_administered=models.DateField(blank=True, null=True)
      
    def __str__(self):
        if self.completed:
             return f"{self.vaccine_name.name} vaccination for {self.animal.name} (completed on {self.date_administered})"
           
        else:
            return f"{self.vaccine_name.name} vaccination for {self.animal.name} (not completed)"
    

