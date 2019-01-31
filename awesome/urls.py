from django.urls import path
from . import views

app_name = 'awesome'

urlpatterns = [
    path('<slug:username>/', views.AccountListView.as_view(), name='user_home'),
    path('<slug:username>/create/', views.AccountCreateView.as_view(), name='account_create'),

]
