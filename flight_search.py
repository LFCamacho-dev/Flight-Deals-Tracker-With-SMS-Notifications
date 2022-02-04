import datetime as dt
import os
import requests
from dateutil.relativedelta import relativedelta
from flight_data import FlightData
from notification_manager import NotificationManager

notification_manager = NotificationManager()


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

    def search_flight(self, fly_to, lowest_price, to_city):

        next_sunday = dt.date.today() + dt.timedelta((4 - dt.date.today().weekday()) % 7)
        six_months = dt.date.today() + relativedelta(months=+6)

        search_params = {
            "fly_from": "DFW",
            "fly_to": fly_to,
            "date_from": next_sunday,
            "date_to": six_months,
            "curr": "USD"
        }

        response = requests.get(url=f"{self.endpoint}/v2/search", params=search_params, headers=self.headers)
        response.raise_for_status()

        if len(response.json()["data"]) == 0:
            print(f"Sorry, no flights available to {to_city}.")
        elif len(response.json()["data"]) >= 0:
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

                try:
                    users = notification_manager.get_emails()
                    emails = [row["email"] for row in users]

                    message = f"Low price alert! Only ${data['price']} to fly from " \
                              f"{data['cityFrom']}-{data['cityCodeFrom']} to {to_city}-{data['cityCodeTo']}, " \
                              f"on {date_split[0]}\n\n"\
                              f"{data['deep_link']}\n\n"
                except Exception as err:
                    print(err)
                else:
                    notification_manager.send_emails(emails, message)

            else:
                print(f"Sorry, flights to {data['cityTo']} are too expensive")
