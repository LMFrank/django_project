# -*- coding: utf-8 -*-
import json
from django.urls import reverse
from celery_tasks import sample_tasks
from unittest.mock import patch, call


def test_index(client):
    url = reverse("celery_tasks:index")
    response = client.get(url)
    assert response.status_code == 200

def test_task():
    assert sample_tasks.create_task.run(1)
    assert sample_tasks.create_task.run(2)
    assert sample_tasks.create_task.run(3)

@patch("celery_tasks.sample_tasks.create_task.run")
def test_mock_task(mock_run):
    assert sample_tasks.create_task.run(1)
    sample_tasks.create_task.run.assert_called_once_with(1)

    assert sample_tasks.create_task.run(2)
    assert sample_tasks.create_task.run.call_count == 2

    assert sample_tasks.create_task.run(3)
    assert sample_tasks.create_task.run.call_count == 3


# Integration test
def test_task_status(client):
    response = client.post(reverse("celery_tasks:run_task"), {"type": 1})
    content = json.loads(response.content)
    task_id = content["task_id"]
    assert response.status_code == 202
    assert task_id

    response = client.get(reverse("celery_tasks:get_status", args=[task_id]))
    content = json.loads(response.content)
    assert content == {
        "task_id": task_id,
        "task_status": "PENDING",
        "task_result": None
    }
    assert response.status_code == 200

    while content["task_status"] == "PENDING":
        response = client.get(reverse("celery_tasks:get_status", args=[task_id]))
        content = json.loads(response.content)

    assert content == {
        "task_id": task_id,
        "task_status": "SUCCESS",
        "task_result": True
    }