from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponse
from .forms import (
    LoginForm,
    RegisterForm,
)
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.signing import TimestampSigner


# Create your views here.
def send_mail(subject,to,template,context):
    html_content = get_template(template).render(context)
    msg = EmailMessage(subject, html_content,to=to,headers={'From':'Awesome'})
    msg.content_subtype = 'html'
    msg.send()

def check_link(request, sign_value):
    signer = TimestampSigner()
    value = signer.sign(sign_value)
    from urllib.parse import urlencode,urlsplit,urlunsplit
    query = urlencode({'token': value.split(':',maxsplit=1)[1]})
    url_c = urlsplit(request.get_raw_uri())

    return urlunsplit((url_c.scheme,url_c.netloc,url_c.path,query,'')) 


def index(request):
    return redirect(reverse('accounts:log_in'))

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # send_mail(user)
            return HttpResponse('login success：{}{}'.format(user.username,request.get_raw_uri()))
        else:
            form.add_error('username','Please enter right account!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = form.cleaned_data['email']
            send_mail('Active account', [email],
                    'accounts/base_message.html',
                    {'link': check_link(request,email)}
                    )
            return HttpResponse('go check email {}'.format(email))
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
    
def active_account(request, token):
    
