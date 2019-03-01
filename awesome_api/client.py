import requests
from urllib.parse import urljoin


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

    def join_url(self, path):
        return urljoin(self.host, path)