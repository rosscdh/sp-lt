import random
import requests

from pyquery import PyQuery as pq
from locust import HttpLocust, TaskSet, task
from urllib.parse import urljoin


BASE_URL = 'https://hispryker.com'

USER_CREDENTIALS = [
    ('liju.rajan@mindcurv.com', 'change123')
]

URLS = (
    '/',
    '/en/cameras-&-camcorders/digital-cameras',
    '/en/canon-ixus-285-9',
    '/en/computers/tablets?price%5Bmin%5D=19&price%5Bmax%5D=950&ipp=12&sort=&q=sony',
    '/en/computers/tablets?price%5Bmin%5D=19&price%5Bmax%5D=950&ipp=12&sort=&q=noone',
    '/en/sony-cyber-shot-dsc-w830-20',
    '/en/search?q=sony',
    '/en/computers/tablets?price%5Bmin%5D=19&price%5Bmax%5D=950&ipp=12&sort=&q=samsung',
    '/en/sony-cyber-shot-dsc-wx220-23',
    '/en/test-404-non-exist',
    '/en/sony-swr50-94',
    '/en/search?q=samsung',
)


class UnauthenticatedBehaviour(TaskSet):
    login_url = '/login_check'

    def get_login_token(self) -> str:
        resp = requests.get(urljoin(self.locust.host, self.login_url))
        page_data = pq(resp.content)
        page_data('#loginForm__token')
        return page_data('#loginForm__token').val()

    @task
    def check_urls(self):
        url = random.choice(URLS)
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 404 and '-404-' in url:
                response.success()


class AuthenticatedBehaviour(UnauthenticatedBehaviour):
    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            user, passw = USER_CREDENTIALS.pop()
            token = self.get_login_token()
            self.client.post(self.login_url, {"loginForm[email]": user, "loginForm[password]": passw, 'loginForm[_token]': token})


# class UserView(HttpLocust):
#     host     = BASE_URL
#     task_set = AuthenticatedBehaviour
#     min_wait = 5000
#     max_wait = 60000


class UnauthenticatedUserView(HttpLocust):
    host     = BASE_URL
    task_set = UnauthenticatedBehaviour
    min_wait = 5000
    max_wait = 60000
