from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.http import HttpResponse
# from rest_framework import viewsets
# from . serializers import UserSerializer, GroupSerializer
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









#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer