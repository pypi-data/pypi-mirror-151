"""email controller

"""
from flask import Flask
from service.email_service import EmailService
from service.bill_service import BillService

app = Flask(__name__)


@app.route('/api/v1/send-bill-notification')
def send_bill_notification():
    """Send email tiwh notification of urgent bill

    Returns:
        _type_: View content
    """
    bill_service = BillService()
    email_service = EmailService()
    bill = bill_service.get_next_bill()
    email_service.send_bill_notification(bill)
    return '<b>Email sent to destination</b>'


app.run()

if __name__ == "__main__":
    send_bill_notification()
