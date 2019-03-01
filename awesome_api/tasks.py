from __future__ import absolute_import
from celery import shared_task
import requests


@shared_task
def fetch(method, url, cookies):
    resp = requests.request(method, url, cookies=cookies)
    return resp.json()
