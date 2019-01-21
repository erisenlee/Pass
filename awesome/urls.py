from django.urls import path
from . import views

app_name = 'awesome'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('register/', views.user_register,name='user_create'),
    path('register/check', views.active_account,name='user_check'),

]
