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
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.signing import dumps,loads

# Create your views here.
def send_mail(subject, to, template, context):
    html_content = get_template(template).render(context)
    msg = EmailMessage(subject, html_content, to=to, headers={'From': 'Awesome'})
    msg.content_subtype = 'html'
    msg.send()


def check_link(request, user):
    from urllib.parse import urlencode, urlsplit, urlunsplit

    query = urlencode({'token': default_token_generator.make_token(user),
                       'user': dumps(user.username)}
                      )
    url_c = urlsplit(request.get_raw_uri())

    return urlunsplit((url_c.scheme, url_c.netloc, url_c.path + 'check', query, ''))


def index(request):
    return redirect(reverse('accounts:log_in'))


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # send_mail(user)
            return redirect('awesome:user_home',args=(user.username,))
        else:
            form.add_error('username', 'Please enter right account!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # form = UserCreationForm(request.POST)
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


def active_account(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        username = loads(request.GET.get('user'))
        if token is None or username is None:
            raise PermissionDenied
        try:
            user = User.objects.get_by_natural_key(username)
        except Exception:
            raise PermissionDenied
        if user is None:
            raise PermissionDenied
        if user.is_active:
            return render(
                request,
                'accounts/register_check.html',
                {'class':'info','message':'Already activated'}
            )
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return render(
                request,
                'accounts/register_check.html',
                {'class':'success','message':'Successfully activated'}
            ) 
        else:
            raise PermissionDenied
    else:
        return redirect(reverse('accounts:user_register'))
