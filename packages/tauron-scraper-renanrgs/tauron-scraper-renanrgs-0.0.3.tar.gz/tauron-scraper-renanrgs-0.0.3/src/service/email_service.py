"""email_service module is responsible for performing email operations
like sending emails regarding bills
"""
import yagmail
from data_model.bill import Bill
from data_model.email_data import GmailCredentials
from util import messages

from service.bill_service import BillService


class EmailService:
    """Service responsible for email operations
    """
    _credentials = GmailCredentials()

    def __init__(self):
        self.mail_session = yagmail.SMTP(
            user=self._credentials.user, password=self._credentials.password)
        self.bill_service = BillService()

    def send(self, subject: str, content: str, attachment=None) -> None:
        """Send email

        Args:
            subject (str): email subject
            content (str): email content
            attachment (_type_, optional): email attachment. Defaults to None.
        """
        self.mail_session.send(to=self._credentials.user,
                               subject=subject, contents=content, attachments=attachment)

    def send_bill_notification(self):
        """Send email in case due date is close as 5 days

        Args:
            bill (Bill): next bill
        """
        if self.bill_service.is_urgent_bill():
            bill = self.bill_service.get_next_bill()
            self.mail_session.send(to=self._credentials.user, subject='Outstanding Bill',
                                   contents=messages.OUTSTANDING_BILL_MSG
                                   .format(bill_amount=bill.amount, due_date=bill.due_date))
