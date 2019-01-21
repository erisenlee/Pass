from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def user_home(request,username):
    user = request.user
    accounts = user.account_set.all()
    return render(request,'awesome/user_home.html',{'accounts':accounts})

