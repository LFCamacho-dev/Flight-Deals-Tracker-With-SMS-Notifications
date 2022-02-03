from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
# from flight_data import FlightData

# This file will need to use the DataManager, FlightSearch,
# FlightData, NotificationManager classes to achieve the program requirements.


# 2- once the AITA was added, search for flights that are cheaper than specified in the spreadsheet.

# 3- if a cheap flight is found, notify the user via sms


data_manager = DataManager()

try:
    with open('destination_data.json') as f:
        print(f.read())
except FileNotFoundError:
    print("File not found, fetching from google sheet...")
    spreadsheet_data = data_manager.read_destinations_sheet()


sms_manager = NotificationManager()
# sms_manager.send_sms()

flight_search = FlightSearch()
# flight_search.get_city_code("Dallas")
# flight_search.search_flight()
#


