from django.contrib import admin
from .models import Service, Consultation, Fee, ConsultationItem


class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'updated_at')
   # search_fields = ('name')


class ConsultationItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('description',)}
    list_display = ( 'type','fee', 'category','is_available', 'updated_at')
    list_filter = ('is_available',)

class FeeAdmin(admin.ModelAdmin):
   
    list_display = ('fee', )
   # search_fields = ('name')
   
   
admin.site.register(Consultation)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ConsultationItem,ConsultationItemAdmin)
