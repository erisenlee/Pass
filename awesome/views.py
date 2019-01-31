from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountForm

class AccountListView(ListView, LoginRequiredMixin):
    template_name = 'awesome/user_home.html'
    paginate_by = 3
    context_object_name = 'account_list'
    def get_queryset(self):
        return self.request.user.account_set.all()

class AccountCreateView(CreateView, LoginRequiredMixin):
    template_name = 'awesome/create.html'
    form_class = AccountForm
    


# @login_required
# def user_home(request,username):
#     user = request.user
#     accounts = user.account_set.all()
#     return render(request,'awesome/user_home.html',{'accounts':accounts})

