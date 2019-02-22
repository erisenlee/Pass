from concurrent.futures import as_completed, ThreadPoolExecutor
import requests
from urllib.parse import urljoin
from datetime import date, timedelta
from django.utils.dateformat import DateFormat
import time
from functools import wraps


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


def get_cookie(login_url, auth):
    resp = requests.post(login_url, data=auth)
    cookie = resp.request.headers['Cookie']
    cookie_dict = {k: v for k, v in [tuple(cookie.split('='))]}
    return cookie_dict


class Client:
    def __init__(self, host, username, password, login_endpoint=None, cookie=True):
        self.host = host if host.startswith('http') else 'http://' + host
        if not login_endpoint:
            login_endpoint = 'fns/login'
        self.login_url = urljoin(self.host, login_endpoint)
        self.username = username
        self.password = password
        self.login_status = False
        # self.cookie = get_cookie(self.login, dict(
        #     username=self.username, password=self.password))
        if not cookie:
            self.session = requests.Session()

    def raw_get(self, url, cookie):
        resp = requests.get(url, cookies=cookie)
        if resp.status_code == 200:
            return resp.json()

    def raw_post(self, url, cookie):
        resp = requests.post(url, cookies=cookie)
        if resp.status_code == 200:
            return resp.json()

    def login(self):
        # print(self.login_url)
        try:
            self.session.post(self.login_url, data=dict(
                username=self.username, password=self.password))
        except Exception:
            print('login failed!')
            return
        self.login_status = True

    def get(self, path=None, url=None, **param):
        resp = None
        self.get_login()
        if url:
            resp = self.session.get(url)
        elif path:
            url, params = self._make_request(path, **param)
            resp = self.session.get(url, params=params)
        else:
            raise ValueError('path or url is needed')
        if resp.status_code == 200:
            return resp.json()

    def post(self, path=None, url=None, **data):
        resp = None
        self.get_login()
        if url:
            data = dict(**data)
            resp = self.session.post(url, data=data)
        elif path:
            url, data = self._make_request(path, **data)
            resp = self.session.post(url, data=data)
        else:
            raise ValueError('path or url is needed')
        if resp.status_code == 200:
            return resp.json()

    def _make_request(self, path, **data):

        if path:
            url = urljoin(self.host, path)
            data = dict(**data)
            return url, data
        else:
            raise ValueError('path is empty')

    def get_login(self):
        if not self.login_status:
            self.login()


def fetch(c, day):
    url = 'http://nc.fengniaojx.com/fns/waybill/waybillList?beginFinishTime={} 00:00:00&endFinishTime={} 23:59:59&rows=0'.format(
        day, day)
    return c.post(url=url)


@timethis
def get_order_count(days):
    today = date.today()
    gen_date = (today - timedelta(days=i) for i in range(1, days+1))
    dates = [DateFormat(date_g).format('Y-m-d') for date_g in gen_date]
    url = 'http://nc.fengniaojx.com/fns/waybill/waybillList?beginFinishTime={} 00:00:00&endFinishTime={} 23:59:59&rows=0'
    gen_urls = (url.format(day, day) for day in dates)

    host = 'nc.fengniaojx.com'
    c = Client(host, 'admin', 'abcd1234')
    cookie = get_cookie(c.login_url, dict(
        username=c.username, password=c.password))
    result = []
    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(
            c.raw_post, url, cookie): url for url in gen_urls}
        for future in as_completed(future_to_url):
            data = future.result()['total']
            result.append(data)
    return result


@timethis
def get_order(days):
    today = date.today()
    gen_date = (today - timedelta(days=i) for i in range(1, days + 1))
    dates = [DateFormat(date_g).format('Y-m-d') for date_g in gen_date]
    host = 'nc.fengniaojx.com'
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


if __name__ == "__main__":
    # result = get_order(20)
    result = get_order_count(20)

    print(result)
