import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object("django.conf:settings", namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
app.conf.broker_connection_retry_on_startup = True

# app.conf.task_routes = {
#     'accounts.tasks.task1': {'queue': 'queue1'},
#     'accounts.tasks.task2': {'queue': 'queue2'},
#     'accounts.tasks.remove_expired_tokens': {'queue':'queue2'},
# }


app.autodiscover_tasks()
print(f"Discovered tasks: {app.tasks.keys()}")
