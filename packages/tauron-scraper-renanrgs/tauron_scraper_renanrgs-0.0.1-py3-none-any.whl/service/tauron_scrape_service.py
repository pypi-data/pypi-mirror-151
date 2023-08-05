from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime

import requests
from data_model.user_data import UserData
from data_model.bill import Bill
from http_adapter.ssl3_http_adapter import Ssl3HttpAdapter
from requests.adapters import HTTPAdapter
from soup.html_parser import HtmlParser
from util.formatter import Util


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


class TauronService:
    def __init__(self, session=TauronSession()):
        self.dashboard_response, self.session = session.login()
        self.parser = HtmlParser(self.dashboard_response.content)
        self.http_adapter = session.http_adapter

    def _navigate(self, url):
        self.session.mount(url, self.http_adapter)
        return self.session.get(url)

    def get_total_debt(self):
        content = self.dashboard_response.content
        return self.parser.get_total_debt(content)

    def get_last_reading(self):
        return self.parser.get_last_reading(self.dashboard_response.content)

    def _next_bill_date_time(self):
        content = self.dashboard_response.content
        date = self.parser.get_next_bill(content).strip()
        date = Util.remove_non_digits(date)
        date = datetime.strptime(date, '%d%m%Y')

        return date

    def is_urgent_bill(self):
        now = datetime.now()
        date = self._next_bill_date_time()
        days_left = (now - date).days
        return True if days_left > -5 else False

    def due_bill_date_str(self, date_format='%d-%m-%Y'):
        return self._next_bill_date_time().strftime(date_format)

    def next_bill_value(self):
        content = self.dashboard_response.content
        float_value = self.parser.get_next_bill_value(content)\
            .replace(',', '.')\
            .replace('zł', '')\
            .strip()
        return float_value

    def get_next_bill(self) -> Bill:
        amount = self.next_bill_value()
        due_date = self.due_bill_date_str()
        return Bill(amount, due_date)
