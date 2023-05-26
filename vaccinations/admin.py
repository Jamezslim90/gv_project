from django.contrib import admin
from vaccinations.models import Vaccination, Vaccine, Disease


class VaccinationAdmin(admin.ModelAdmin):
    list_display = ( 'vaccine_name', 'animal', 'date_administered', 'completed')
  

class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'dosage','expiration_period')
    
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type')
    
      
admin.site.register(Vaccination, VaccinationAdmin)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Disease, DiseaseAdmin)