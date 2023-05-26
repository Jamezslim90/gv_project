from .models import Appointment

def get_notification(request):
    count = Appointment.objects.all().count()
    data = {
        "count":count
    }
    return data


from notifications.models import CustomerNotification
def cusnotifications(request):
    sentNotifications = CustomerNotification.objects.filter(sent=True)
    return {'cusnotifications': sentNotifications}