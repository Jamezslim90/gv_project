from django.contrib import admin
from doctors.models import Doctor, AnimalSpecialty, OpeningHour, BankAccount, Meeting


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'VCN_number', 'is_approved', 'created_at', 'experience', 'state_of_practice', )
    list_display_links = ('user',)
    list_editable = ('is_approved',)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'from_hour', 'to_hour')
    
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'bank_name', 'account_number', 'account_name')
    
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'topic','customer_email','duration','timezone','zoom_id')
    
    
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(AnimalSpecialty)
admin.site.register(OpeningHour, OpeningHourAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Meeting, MeetingAdmin)


# 'get_specialties'