from bs4 import BeautifulSoup


class HtmlParser:

    def __init__(self, content=None):
        self.parser = BeautifulSoup(content, 'html.parser') if content else BeautifulSoup('', 'html.parser')

    def get_total_debt(self, content):
        self.parser.markup = content
        return self.parser.find('span', attrs={'class': 'amountInfo red'}).text

    def get_last_reading(self, content):
        self.parser.markup = content
        return self.parser.find('span', attrs={'class': 'scale'}).text

    def get_next_bill(self, content):
        self.parser.markup = content
        return self.parser.find('span', attrs={'class': 'paymentDate'}).text

    def get_next_bill_value(self, content):
        self.parser.markup = content
        return self.parser.select_one('body > div.content > div > div.columnLong > section.moduleSeparator.clearfix > '
                                      'div.lastInvoiceList.clearfix > div:nth-child(1) > span.ammount.red').text
