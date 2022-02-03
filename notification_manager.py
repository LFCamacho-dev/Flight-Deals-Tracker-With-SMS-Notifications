import os
from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.api_key = os.environ.get("APIKEY")
        self.account_sid = os.environ.get("ACC_SID")
        self.auth_token = os.environ.get("AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self):

        message = self.client.messages.create(
            to=os.environ.get("TO_TEL"),
            from_=os.environ.get("FROM_TEL"),
            body=f"TESTING\n"
                 f"Just making sure it works :)\n"
        )

        print(f"the ID is: {message.sid}, and the status is: {message.status}")
