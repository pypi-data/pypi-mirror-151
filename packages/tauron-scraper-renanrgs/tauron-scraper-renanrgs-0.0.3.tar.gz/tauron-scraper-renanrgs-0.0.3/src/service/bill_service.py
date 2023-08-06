from datetime import datetime

from data_model.bill import Bill
from session.session import TauronSession
from soup.html_parser import HtmlParser
from util.formatter import Util


class BillService:
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

    def next_due_bill_datetime(self):
        content = self.dashboard_response.content
        date = self.parser.get_next_bill(content).strip()
        date = Util.remove_non_digits(date)
        date = datetime.strptime(date, '%d%m%Y')

        return date

    def is_urgent_bill(self):
        now = datetime.now()
        date = self.next_due_bill_datetime()
        days_left = (now - date).days
        return True if days_left > -5 else False

    def due_bill_date_str(self, date_format='%d-%m-%Y'):
        return self.next_due_bill_datetime().strftime(date_format)

    def next_bill_value(self):
        content = self.dashboard_response.content
        float_value = self.parser.get_next_bill_value(content)\
            .replace(',', '.')\
            .replace('zł', '')\
            .strip()
        return float_value # TODO Use Decimal or Int instead of float for monetary values

    def get_next_bill(self) -> Bill:
        amount = self.next_bill_value()
        due_date = self.due_bill_date_str()
        return Bill(amount, due_date)
