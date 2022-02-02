import os
import requests

# This class is responsible for talking to the Google Sheet.


class DataManager:

    def __init__(self):
        self.SHEET_AUTH = os.environ.get("SHEET_AUTH")
        self.ENDPOINT = "https://api.sheety.co/bf637b0f90dd7856fb44c4190b0e1659/flightDeals/prices"

        self.headers = {
            "Authorization": self.SHEET_AUTH,
        }

    def read_flight_sheet(self):
        response = requests.get(url=self.ENDPOINT, headers=self.headers)
        response.raise_for_status()
        data = response.text
        print(data)

