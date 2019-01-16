from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.log_in, name='log_in'),
    # path('register/', views.register),

]
