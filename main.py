from data_manager import DataManager
from notification_manager import NotificationManager

# This file will need to use the DataManager, FlightSearch,
# FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
data_manager.read_flight_sheet()

sms_manager = NotificationManager()
# sms_manager.send_sms()



