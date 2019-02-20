from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponse
from .forms import (
    LoginForm,
    RegisterForm,
)
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.exceptions import PermissionDenied

from .models import Token

# Create your views here.
def send_mail(subject, to, template, context):
    html_content = get_template(template).render(context)
    msg = EmailMessage(subject, html_content, to=to, headers={'From': 'Awesome'})
    msg.content_subtype = 'html'
    msg.send()


def check_link(request, user):
    token= Token(user=user)
    token.save()
    path = reverse('accounts:confirm_email', kwargs={"token": token.key})
    url = request.build_absolute_uri(path)
    return url

def index(request):
    return redirect(reverse('accounts:log_in'))


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
            # send_mail(user)
                return redirect('awesome:user_home',username=user.username)
            else:
                form.add_error('username', 'Please enter right account!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = form.cleaned_data['email']
            send_mail('Active account', [email],
                      'accounts/base_message.html',
                      {'link': check_link(request, user)}
                      )
            return HttpResponse('go check email {}'.format(email))
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def active_account(request,token):
    if request.method == 'GET':
        key = token
        if key is None:
            raise PermissionDenied
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Exception:
            raise PermissionDenied
        user = token.user
        if not token.timevalid():
            token.delete()
            user.delete()
            return render(
                request,
                'accounts/register_check.html',
                {'class':'warning','message':'Invalid link'}
            )
        if user.is_active:
            return render(
                request,
                'accounts/register_check.html',
                {'class':'info','message':'Already activated'}
            )
        
        user.is_active = True
        user.save()

        return render(
            request,
            'accounts/register_check.html',
            {'class':'success','message':'Successfully activated'}
        ) 
    else:
        return redirect(reverse('accounts:user_register'))
