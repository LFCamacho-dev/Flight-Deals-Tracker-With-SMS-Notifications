import os
import requests
from pprint import pprint


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.apikey = os.environ.get("TEQUILA_APIKEY")
        self.endpoint = "https://tequila-api.kiwi.com"

        self.headers = {
            "apikey": self.apikey,
            "Content-Encoding": "gzip"
        }

        self.search_params = {
            "fly_from": "LON",
            "fly_to": "airport:DFW",
            "date_from": "03/02/2022",
            "date_to": "04/02/2022",
            "curr": "USD"
        }

    def get_city_code(self, city):
        location_params = {"term": f"{city}"}
        response = requests.get(url=f"{self.endpoint}/locations/query", params=location_params, headers=self.headers)
        response.raise_for_status()
        code_data = response.json()["locations"][0]["code"]
        print(f"Returning code: {code_data}")
        return code_data

    def search_flight(self):
        response = requests.get(url=f"{self.endpoint}/v2/search", params=self.search_params, headers=self.headers)
        response.raise_for_status()
        data = response.json()["data"]
        pprint(data)

