from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponse
from .forms import LoginForm
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.signing import TimestampSigner

# Create your views here.
def send_mail(user):
    subject = 'Import Info'

    # context = {
    #     'host': request.host,
    #
    # }
    html_content = get_template('accounts/message.html').render({'user':user})
    fromemal = 'lm.liu@fengniaojx.com'
    to = ['abnormalboy@126.com']
    msg = EmailMessage(subject, html_content, fromemal, to)
    msg.content_subtype = 'html'
    msg.send()


def index(request):
    return redirect(reverse('accounts:log_in'))



def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                send_mail(user)
                return HttpResponse('login success：{}'.format(user.username))
            else:
                form.add_error('username','Please enter right account!')
                return render(request, 'accounts/login.html', {'form':form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
