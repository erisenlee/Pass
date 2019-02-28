import aiohttp
import asyncio
from urllib.parse import urljoin
from datetime import date, timedelta
from django.utils.dateformat import DateFormat
import time
import requests
from functools import wraps, partial


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


class Client:
    """docstring for Client."""

    def __init__(self, host, username, password, login_endpoint=None, cookie=None):
        self.host = host if host.startswith('http') else 'http://' + host
        if not login_endpoint:
            login_endpoint = 'fns/login'
        self.login_url = urljoin(self.host, login_endpoint)
        self.auth = dict(username=username, password=password)
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


@timethis
async def login(c):
    async with aiohttp.ClientSession() as session:
        async with session.post(c.login_url, data=c.auth) as resp:
            async with resp:
                assert resp.status == 200
                cookie_str = resp.request_info.headers.get('cookie')
                return {k: v for k, v in [tuple(cookie_str.split('='))]}


async def fetch(method, session, url, cookies):
    async with session.request(method, url, cookies=cookies) as resp:
        return await resp.json()


async def get_order(days, c):
    today = date.today()
    gen_date = (today - timedelta(days=i) for i in range(1, days + 1))
    dates = [DateFormat(date_g).format('Y-m-d') for date_g in gen_date]
    path = 'fns/waybill/waybillList?beginFinishTime={} 00:00:00&endFinishTime={} 23:59:59&rows=0'
    urls = [path.format(day, day) for day in dates]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for key, url in enumerate(urls):

            task = asyncio.create_task(
                fetch('POST', session, c.url_join(url), c.cookie))
            task.add_done_callback(partial(callback, key=key))
            tasks.append(task)
        futures, _ = await asyncio.wait(tasks)
        results = []
        for f in futures:
            data = f.result()
            results.append(data)
        return results


def callback(future, key=None):
    result = future.result()
    result['key'] = key


@timethis
def main():
    c = Client('fns.livejx.cn', 'admin', 'abcd1234')
    loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(login(c))
    result = loop.run_until_complete(get_order(10, c))
    return result


if __name__ == "__main__":
    main()
