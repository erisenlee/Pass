from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('register/', views.user_register, name='user_create'),
    path('register/confirm_email/<str:token>/', views.active_account, name='confirm_email'),
    

]
