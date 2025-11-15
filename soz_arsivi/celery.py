import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soz_arsivi.settings")

app = Celery("soz_arsivi")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(['statements.ai'])
