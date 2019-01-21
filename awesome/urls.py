from django.urls import path
from . import views

app_name = 'awesome'

urlpatterns = [
    path('<slug:username>', views.user_home, name='user_home'),
    # path('accounts/create', views.index, name='index'),

]
