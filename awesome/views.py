from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountForm

def client_processor(request):
    context = {
        'ip_addr': request.META['REMOTE_ADDR'],
        'host_name': request.META['REMOTE_HOST'],
        'extra' : 'processor'
    }
    return context


class AccountListView(ListView, LoginRequiredMixin):
    template_name = 'awesome/user_home.html'
    paginate_by = 3
    context_object_name = 'account_list'
    context_processors = [client_processor]

    def get_queryset(self):
        return self.request.user.account_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unsafe'] = " <script>alert('hello')</script>"
        return context

class AccountCreateView(CreateView, LoginRequiredMixin):
    template_name = 'awesome/create.html'
    form_class = AccountForm
    


@login_required
def user_home(request,username):
    user = request.user
    accounts = user.account_set.all()
    return render(request,'awesome/user_home.html',{'accounts':accounts})

