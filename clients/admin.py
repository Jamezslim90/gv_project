from django.contrib import admin
from clients.models import Animal, Appointment, AnimalType, Category, Symptom


class AnimalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'animal_slug': ('name',)}
    list_display = ('name', 'animal_category', 'owner','age', 'last_vaccination_date' )
  

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'animal_category', 'animal', 'appointment_type', 'date','time')
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'animal_category',)
    
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ( 'category', 'animal_type')    
    
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AnimalType, AnimalTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Symptom, SymptomAdmin)

# 'get_specialties'

