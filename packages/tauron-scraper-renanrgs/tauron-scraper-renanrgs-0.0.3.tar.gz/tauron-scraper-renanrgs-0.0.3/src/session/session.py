from abc import ABC, abstractmethod
from dataclasses import asdict

import requests
from data_model.user_data import UserData
from http_adapter.ssl3_http_adapter import Ssl3HttpAdapter
from requests.adapters import HTTPAdapter


class Session(ABC):

    @abstractmethod
    def login(self):
        pass


class TauronSession(Session):

    def __init__(self, http_adapter: HTTPAdapter = Ssl3HttpAdapter()):
        self.url = 'https://logowanie.tauron.pl/login'
        self.http_adapter = http_adapter
        self.session = requests.Session()
        self.session.mount(self.url, adapter=self.http_adapter)

    def login(self):
        response = self.session.post(
            self.url, cookies={'PHPSESSID': ''}, data=asdict(UserData()), allow_redirects=False)
        response = self._manage_redirects(self.session, response)
        return response, self.session

    def _manage_redirects(self, session, response):
        while response.next:
            session.mount(response.next.url, self.http_adapter)
            response = session.get(response.next.url, allow_redirects=False)
        return response
