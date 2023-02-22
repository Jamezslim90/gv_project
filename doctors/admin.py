from django.contrib import admin
from doctors.models import Doctor, AnimalSpecialty #OpeningHour


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vcn_number', 'is_approved', 'created_at')
    list_display_links = ('user',)
    list_editable = ('is_approved',)


# class OpeningHourAdmin(admin.ModelAdmin):
#     list_display = ('vendor', 'day', 'from_hour', 'to_hour')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(AnimalSpecialty)
#admin.site.register(OpeningHour, OpeningHourAdmin)