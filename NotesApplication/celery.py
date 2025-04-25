import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotesApplication.settings')
app = Celery('NotesApplication')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bing=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'check-remove-files': {
        'task': 'files.tasks.check_remove_files',
        'schedule': 60.0, #* 60.0,
    },
}

app.conf.timezone = 'Europe/Warsaw'