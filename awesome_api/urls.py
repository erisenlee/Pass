from django.urls import path
from . import views


app_name = 'awesome_api'

urlpatterns = [
    path('<str:username>/run/', views.run_tasks, name='run_tasks'),
]