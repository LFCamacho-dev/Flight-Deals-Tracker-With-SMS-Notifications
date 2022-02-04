import json
from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch

data_manager = DataManager()
flight_search = FlightSearch()
sms_manager = NotificationManager()

try:
    with open('destination_data.json') as data_file:
        data = json.load(data_file)
        for entry in data:
            # print(entry["iataCode"])
            flight_search.search_flight(entry["iataCode"], entry["lowestPrice"])

except FileNotFoundError:
    print("File not found, fetching from google sheet...")
    spreadsheet_data = data_manager.read_destinations_sheet()
