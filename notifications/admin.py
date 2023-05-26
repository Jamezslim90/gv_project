from django.contrib import admin
from .models import DoctorNotification, CustomerNotification

# Register your models here.


class CustomerNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'broadcast_on', 'sent')
    
admin.site.register(CustomerNotification)


class DoctorNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'broadcast_on', 'sent')
    
admin.site.register(DoctorNotification)
