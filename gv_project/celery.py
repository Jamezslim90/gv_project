from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gv_project.settings')

app = Celery('gv_project')
app.conf.enable_utc = False
app.conf.update(timezone='Africa/Lagos')
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery beat scheduler

app.conf.beat_schedule = {

}   




# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')