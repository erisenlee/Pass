from django.shortcuts import render
from django.contrib.auth.views import login_required
# Create your views here.


@login_required
def user_home(request):
    user = request.user
    accounts = user.account_set.all()
    return render(request,'awesome/user_home.html',{'accounts':accounts})

