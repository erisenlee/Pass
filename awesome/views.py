from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from pyecharts import Line

from .forms import AccountForm
from .utils import get_order
from .models import Account


class AccountListView(ListView):
    template_name = 'awesome/user_home.html'
    # paginate_by = 5
    # context_object_name = 'account_list'
    # context_processors = [client_processor]
    # ordering = ''
    
    def get_queryset(self):
        return self.request.user.account_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        return context
    

class AccountCreateView(CreateView, LoginRequiredMixin):
    template_name = 'awesome/create.html'
    form_class = AccountForm
    context_object_name = 'account_form'


@login_required
def dash_page(request, username):
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"
    line = linechart()
    context = dict(
        myechart=line.render_embed(),
        host=REMOTE_HOST,
        script_list=line.get_js_dependencies(),
        email=request.user.email,
    )
    return render(request, 'awesome/dash.html', context)


@login_required
def dash(request, username):
    result = {day: value for day, value in get_order(15)}
    return JsonResponse({'data': result})


def linechart():
    host = 'http://fns.livejx.cn'
    result = {day: value for day, value in get_order(15, host)}
    attr = list(result.keys())
    v1 = list(result.values())
    line = Line("Options of data", title_pos='center',title_top='top')
    line.add(
        "Order", attr, v1,
        is_smooth=True,
        is_xaxislabel_align=True,
        is_more_utils=True,
        xaxis_name='Date',
        xaxis_name_pos='end',
        xaxis_name_gap=15,
        yaxis_name='Number',
        yaxis_name_pos='end',
        yaxis_name_gap=15,
        xaxis_interval=0,
        xaxis_rotate=90,
        legend_pos='right',
        legend_top='top',
        mark_line=["max", "average"]
    )
    return line


@login_required
def run_tasks(request, username):
    from awesome.utils import get_order_task
    host = 'fns.livejx.cn'
    result = get_order_task(10, host)
    return JsonResponse(result, safe=False)