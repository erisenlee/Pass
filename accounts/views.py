from django.shortcuts import render
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from .forms import LoginForm


# Create your views here.


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('login success：{}'.format(user.username))
            else:
                form.add_error('username','Please enter right account!')
                return render(request, 'accounts/login.html', {'form':form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
