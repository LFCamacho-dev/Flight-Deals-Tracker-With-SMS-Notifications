import os
import requests


class UserManager:
    def __init__(self, first_name, last_name, confirmed_email):
        self.first_name = first_name
        self.last_name = last_name
        self.confirmed_email = confirmed_email

        self.SHEET_AUTH = os.environ.get("SHEET_AUTH")
        self.ENDPOINT = "https://api.sheety.co/bf637b0f90dd7856fb44c4190b0e1659/flightDeals/users"

        self.headers = {
            "Authorization": self.SHEET_AUTH,
            "Content -Type": "application / json",
        }

        self.params = {
            "user": {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.confirmed_email,
            }
        }

    def upload_user(self):
        response = requests.post(url=self.ENDPOINT, json=self.params, headers=self.headers)
        response.raise_for_status()

        print("Success, your email has been added, look forward to our emails :)")
