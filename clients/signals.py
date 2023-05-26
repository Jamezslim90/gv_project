from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import  Animal
from vaccinations.models import Vaccination , Vaccine 



@receiver(post_save, sender=Animal)
def post_save_create_vaccination_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        # vaccines = instance.animal.vaccine_set.all()
        vaccines = Vaccine.objects.filter(animal_type=instance.animal)
        for vaccine in vaccines:
            Vaccination.objects.create(vaccine_name=vaccine, animal=instance)
    else :
        print('not created')
   

# @receiver(post_save, sender=Animal)
# def create_vaccinations(sender, instance, created, **kwargs):
#     if created:
#         vaccines = instance.animal.vaccine_set.all()
#         for vaccine in vaccines:
#             Vaccination.objects.create(vaccine_name=vaccine, animal=instance)
