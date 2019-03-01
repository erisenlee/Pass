from __future__ import absolute_import
from celery import shared_task
import requests

@shared_task
def add(x, y):
    return x + y

@shared_task
def fetch_task(url, cookies=None):
    resp = requests.post(url, cookies=cookies)
    return resp.json()