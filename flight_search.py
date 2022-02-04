import os
import requests
import datetime as dt
from dateutil.relativedelta import relativedelta
from flight_data import FlightData


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.apikey = os.environ.get("TEQUILA_APIKEY")
        self.endpoint = "https://tequila-api.kiwi.com"

        self.headers = {
            "apikey": self.apikey,
            "Content-Encoding": "gzip"
        }

    def get_city_code(self, city):
        location_params = {"term": f"{city}"}
        response = requests.get(url=f"{self.endpoint}/locations/query", params=location_params, headers=self.headers)
        response.raise_for_status()
        code_data = response.json()["locations"][0]["code"]
        print(f"Returning code: {code_data}")
        return code_data

    def search_flight(self, fly_to, lowest_price):

        next_sunday = dt.date.today() + dt.timedelta((4 - dt.date.today().weekday()) % 7)
        six_months = dt.date.today() + relativedelta(months=+6)

        search_params = {
            # "fly_from": "LON",
            # "fly_to": fly_to,
            "fly_from": "DFW",
            "fly_to": fly_to,
            "date_from": next_sunday,
            "date_to": six_months,
            "curr": "USD"
        }

        response = requests.get(url=f"{self.endpoint}/v2/search", params=search_params, headers=self.headers)
        response.raise_for_status()
        data = response.json()["data"][0]

        if data["price"] < lowest_price:
            date_split = data['local_departure'].split("T")
            print(f"I want to go to {data['cityTo']} and pay no more than: "
                  f"${lowest_price}, current price: ${data['price']}, on {date_split[0]} \n\n"
                  f"Visit: {data['deep_link']}")

            new_flight = FlightData(
                data['price'],
                data['cityFrom'],
                data['cityCodeFrom'],
                data['cityTo'],
                data['cityCodeTo'],
                date_split[0],
                data['deep_link'],
            )

            new_flight.send_alert()

        else:
            print(f"Sorry, flights to {data['cityTo']} are too expensive")
