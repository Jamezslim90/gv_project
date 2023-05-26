from django.contrib import admin
from laboratories.models import Laboratory, Service, Branch

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

class BranchAdmin(admin.ModelAdmin):
    list_display= ('lab','address', 'phone_number', 'email', 'city', 'state',)
    
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('type',)  
      
admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Branch, BranchAdmin)
