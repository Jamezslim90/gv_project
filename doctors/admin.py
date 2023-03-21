from django.contrib import admin
from doctors.models import Doctor, AnimalSpecialty, OpeningHour, BankAccount


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vcn_number', 'is_approved', 'created_at', 'state_of_practice', )
    list_display_links = ('user',)
    list_editable = ('is_approved',)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'from_hour', 'to_hour')
    
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'bank_name', 'account_number', 'account_name')
    
    
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(AnimalSpecialty)
admin.site.register(OpeningHour, OpeningHourAdmin)
admin.site.register(BankAccount, BankAccountAdmin)


# 'get_specialties'