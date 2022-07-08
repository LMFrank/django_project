# -*- coding: utf-8 -*-
from celery import Celery


import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

celery_app = Celery("library",)
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks(['celery_tasks.sms'])