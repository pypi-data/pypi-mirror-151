from service.email_service import EmailService

from service.bill_service import BillService
from datetime import datetime


def send_bill_notification():
    # while True:
        # current_time = datetime.now()
    # if current_time.hour == 8 and current_time.minute == 30:
    bill_service = BillService()
    email_service = EmailService()
    bill = bill_service.get_next_bill()
    email_service.send_bill_notification(bill)


if __name__ == "__main__":
    send_bill_notification()
