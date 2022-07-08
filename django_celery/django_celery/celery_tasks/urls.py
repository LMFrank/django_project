# -*- coding: utf-8 -*-
from django.urls import path
from celery_tasks import views


app_name = 'celery_tasks'
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.run_task, name="run_task"),
    path("tasks/<task_id>/", views.get_status, name="get_status")
]