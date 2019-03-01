from django.urls import path
from . import views

app_name = 'awesome'

urlpatterns = [
    path('<str:username>/home/', views.AccountListView.as_view(), name='user_home'),
    # path('<slug:username>/<int:page>/', views.AccountListView.as_view(), name='user_home'),
    # path('<slug:username>/', views.user_home, name='user_home'),
    path('<str:username>/create/',
         views.AccountCreateView.as_view(), name='account_create'),

    path('<str:username>/dash/', views.dash_page, name='dash_home'),
    path('<str:username>/run/', views.run_tasks, name='run_tasks'),



]
