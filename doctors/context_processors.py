# from clients.models import Appointment

# def get_notification(request):
#     count = Appointment.objects.all().count()
#     data = {
#         "count":count
#     }
#     return data



from notifications.models import DoctorNotification
def docnotifications(request):
    sentNotifications = DoctorNotification.objects.filter(sent=True)
    return {'docnotifications': sentNotifications}