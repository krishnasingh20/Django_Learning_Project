import os 
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "dhs2026.settings"
)

app = Celery("dhs2026")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()