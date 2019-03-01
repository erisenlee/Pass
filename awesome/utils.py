from concurrent.futures import as_completed, ThreadPoolExecutor
import requests
from urllib.parse import urljoin
from datetime import date, timedelta
from django.utils.dateformat import DateFormat
import time
from functools import wraps
from awesome.tasks import fetch_task


class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._start = None
        self._func = func

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started!')
        self._start = self._func()

    def stop(self):
        if self._start == None:
            raise RuntimeError('Not started!')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def timethis(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = Timer()
        t.start()
        result = func(*args, **kwargs)
        t.stop()
        print('{} time spend: {}'.format(func.__name__, t.elapsed))
        return result
    return wrapper


@timethis
def get_cookie(login_url, auth):
    resp = requests.post(login_url, data=auth)
    cookie = resp.request.headers['Cookie']
    cookie_dict = {k: v for k, v in [tuple(cookie.split('='))]}
    return cookie_dict


class Client:
    def __init__(self, host, username, password, login_endpoint=None, cookie=None):
        self.host = host if host.startswith('http') else 'http://' + host
        if not login_endpoint:
            login_endpoint = 'fns/login'
        self.login_url = urljoin(self.host, login_endpoint)
        self.auth = dict(username=username, password=password)
        self.login_status = False
        if not cookie:
            self.cookie = self.get_cookie(self.login_url, self.auth)
        else:
            self.cookie = cookie

    @timethis
    def get_cookie(self, login_url, auth):
        resp = requests.post(login_url, data=auth)
        try:
            cookie = resp.request.headers['Cookie']
        except KeyError:
            raise
        cookie_dict = {k: v for k, v in [tuple(cookie.split('='))]}
        return cookie_dict

    def url_join(self, path):
        return urljoin(self.host, path)

    def raw_get(self, path):
        url = self.url_join(path)
        resp = requests.get(url, cookies=self.cookie)
        if resp.status_code == 200:
            return resp.json()

    def raw_post(self, path):
        url = self.url_join(path)
        resp = requests.post(url, cookies=self.cookie)
        if resp.status_code == 200:
            return resp.json()


def fetch(c, day):
    url = 'fns/waybill/waybillList?beginFinishTime={} 00:00:00&endFinishTime={} 23:59:59&rows=0'.format(
        day, day)
    return c.raw_post(url)


@timethis
def get_order(days, host):
    today = date.today()
    gen_date = (today - timedelta(days=i) for i in range(1, days + 1))
    dates = [DateFormat(date_g).format('Y-m-d') for date_g in gen_date]
    c = Client(host, 'admin', 'abcd1234')
    result = []
    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(
            fetch, c, day): day for day in dates}
        future_map = as_completed(future_to_url)
        for future in future_map:
            data = future.result()['total']
            day = future_to_url[future]
            result.append((day, data))
    result.sort()
    return result


def get_order_task(days, host):
    today = date.today()
    gen_date = (today - timedelta(days=i) for i in range(1, days + 1))
    dates = [DateFormat(date_g).format('Y-m-d') for date_g in gen_date]
    c = Client(host, 'admin', 'abcd1234')
    cookies = c.cookie
    task = fetch_task.s(cookies=cookies)
    result = []
    for day in dates:
        path = 'fns/waybill/waybillList?beginFinishTime={} 00:00:00&endFinishTime={} 23:59:59&rows=0'.format(
            day, day)
        url = c.url_join(path)
        resp = task.delay(url).get()
        result.append(resp)
    return result
 
if __name__ == "__main__":
    # result = get_order(20)
    host = 'http://fns.livejx.cn'
    get_order_task(10, host)

    # print(result)
