from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
import os
from celery.schedules import crontab
from django import setup

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()
app = Celery('config')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Set the Celery beat scheduler to operate in the 'Asia/Kolkata' time zone
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# Add the schedule for the Celery beat scheduler
app.conf.beat_schedule = {
    'fetch_videos': {
        'task': 'videos.tasks.get_latest_videos',
        'schedule': 10.0, # Run the task every 10 seconds  
    },
}