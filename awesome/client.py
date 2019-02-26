import aiohttp
import asyncio
import requests
from urllib.parse import urljoin
from functools import partial


class Client:
    def __init__(self, host, username, password, login_endpoint=None):
        self.host = host if host.startswith('http') else 'http://' + host
        if not login_endpoint:
            login_endpoint = 'fns/login'
        self.login_url = urljoin(self.host, login_endpoint)
        self.auth = dict(username=username, password=password)
        self.cookies = self.get_cookie()

    def get_cookie(self):
        resp = requests.post(self.login_url, data=self.auth)
        try:
            cookie = resp.request.headers['Cookie']
        except KeyError:
            raise
        cookie_dict = {k: v for k, v in [tuple(cookie.split('='))]}
        return cookie_dict

    def task_callback(self, future, key):
        result = future.result()
        result['key'] = key

    async def fetch(self, method, session, url):
        async with session.request(method, url, cookies=self.cookies) as resp:
            await resp.json()

    async def create_tasks(self, apis_gen):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for api in apis_gen():
                task = asyncio.create_task(
                    self.fetch(api.method, session, api.url)
                )
                task.add_done_callback(
                    partial(self.task_callback, key=api.key))
                tasks.append(task)
            futures, _ = await asyncio.wait(tasks)
            return [f.result() for f in futures]

    def run(self, apis_gen):
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self.create_tasks(apis_gen))
        loop.close()
        return results


if __name__ == "__main__":
    host = 'http://fns.livejx.cn'
    c = Client(host, 'admin', 'abcd1234')
    c.run(c.login())
    print(c)
