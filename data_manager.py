import os
import requests
import json
from flight_search import FlightSearch

flight_search = FlightSearch()


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.SHEET_AUTH = os.environ.get("SHEET_AUTH")
        self.ENDPOINT = "https://api.sheety.co/bf637b0f90dd7856fb44c4190b0e1659/flightDeals/prices"
        self.destination_data = {}
        self.is_modified = False

        self.headers = {
            "Authorization": self.SHEET_AUTH,
            "Content -Type": "application / json",
        }

        self.params = {
            "prices": {
                "aitaCode": "ABC",
            }
        }

    def read_destinations_sheet(self):
        response = requests.get(url=self.ENDPOINT, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        for city in data["prices"]:
            if city["iataCode"] == "":
                code = flight_search.get_city_code(city["city"])
                new_data = {
                    "price": {
                        "iataCode": code,
                    }
                }
                response = requests.put(url=f"{self.ENDPOINT}/{city['id']}", json=new_data, headers=self.headers)
                self.is_modified = True
                print(response.text)

        if self.is_modified:
            print("File was modified, fetching data again")
            response = requests.get(url=self.ENDPOINT, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            self.destination_data = data["prices"]
        else:
            print("File was not modified, using original data")
            self.destination_data = data["prices"]

        with open('destination_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.destination_data, f, ensure_ascii=False, indent=4)
