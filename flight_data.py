import os
from notification_manager import NotificationManager

notification = NotificationManager()


class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, price, from_city, from_code, to_city, to_code, departure_date, deep_link):
        self.price = price
        self.from_city = from_city
        self.from_code = from_code
        self.to_city = to_city
        self.to_code = to_code
        self.departure_date = departure_date
        self.deep_link = deep_link
        # self.stop_overs = stop_overs
        # self.via_city = via_city

    def send_alert(self):
        message = notification.client.messages.create(
            to=os.environ.get("TO_TEL"),
            from_=os.environ.get("FROM_TEL"),
            body=f"Low price alert! Only ${self.price} to fly from {self.from_city}-{self.from_code} "
                 f"to {self.to_city}-{self.to_code}, on {self.departure_date}\n"
                 f"{self.deep_link}"
        )

        print(f"the ID is: {message.sid}, and the status is: {message.status}")
