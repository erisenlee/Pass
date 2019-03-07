from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from . serializers import TestCaseSerializer
from .models import TestCase,Task
from .client import Client
from .tasks import fetch



def run_tasks(request, username):
    task = Task.objects.all().first()
    env = task.task_env
    cases = task.task_cases.all()
    c = Client(env.env_host,env.env_login_username,env.env_login_password)
    # s = fetch.s(cookies=c.cookies)
    for case in cases.iterator():

        fetch.apply_async(args=(case.case_method, c.join_url(case.case_path), c.cookies), task_id=case.case_no)
    return HttpResponse('run success')



class TestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer


