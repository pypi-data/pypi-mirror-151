from data_model.bill import Bill
from util import messages
import yagmail

from data_model.email_data import GmailCredentials


class EmailService:

    _credentials = GmailCredentials()

    def __init__(self):
        self.mail_session = yagmail.SMTP(
            user=self._credentials.user, password=self._credentials.password)

    def send(self, subject: str, content: str, attachment=None) -> None:
        self.mail_session.send(to=self._credentials.user,
                               subject=subject, contents=content, attachments=attachment)

    def send_bill_notification(self, bill: Bill):

        self.mail_session.send(to=self._credentials.user, subject='Outstanding Bill',
                               contents=messages.OUTSTANDING_BILL_MSG.format(bill_amount=bill.amount, due_date=bill.due_date))
