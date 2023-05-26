from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json



class CustomerNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=CustomerNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="customer-notification-"+str(instance.id), task="notifications.tasks.customer_broadcast_notification", args=json.dumps((instance.id,)))

    #if not created:



class DoctorNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=DoctorNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="doctor-notification-"+str(instance.id), task="notifications.tasks.doctor_broadcast_notification", args=json.dumps((instance.id,)))

    #if not created: