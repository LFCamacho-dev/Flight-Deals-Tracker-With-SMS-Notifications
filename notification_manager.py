import os
import smtplib
import requests
from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        # region TWILIO AUTH
        self.api_key = os.environ.get("APIKEY")
        self.account_sid = os.environ.get("ACC_SID")
        self.auth_token = os.environ.get("AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)
        # endregion TWILIO AUTH
        # region MAIL AUTH
        self.SHEET_AUTH = os.environ.get("SHEET_AUTH")
        self.ENDPOINT = "https://api.sheety.co/bf637b0f90dd7856fb44c4190b0e1659/flightDeals/users"
        self.headers = {
            "Authorization": self.SHEET_AUTH,
            "Content -Type": "application / json",
        }
        self.email = os.environ.get("email")
        self.password = os.environ.get("password")
        self.SMTP_SERVER = "smtp.gmail.com"
        self.PORT = 587
        self.SSL_PORT = 465
        # endregion MAIL AUTH

    def send_emails(self, emails, message):

        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SSL_PORT) as connection:
            connection.login(user=self.email, password=self.password)
            for email in emails:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject: New Low Price Flight!\n\n {message}"
                )

        print(f"Alert email sent!")

    def get_emails(self):
        response = requests.get(url=self.ENDPOINT, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        customer_data = data["users"]
        return customer_data
