import json
from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
from user_manager import UserManager

data_manager = DataManager()
flight_search = FlightSearch()
sms_manager = NotificationManager()
# user_manager = None


def start_here():
    user_choice = input("What would you like to do? (new user / search flights): ")

    if user_choice == "search flights":
        try:
            with open('destination_data.json') as data_file:
                data = json.load(data_file)
                for entry in data:
                    # print(entry["iataCode"])
                    flight_search.search_flight(entry["iataCode"], entry["lowestPrice"])

        except FileNotFoundError:
            print("File not found, fetching from google sheet... please try again once it's done")
            spreadsheet_data = data_manager.read_destinations_sheet()

        finally:
            start_here()

    elif user_choice == "new user":
        first_name = input("What is your first name?: ")
        last_name = input("What is your last name?: ")

        def confirm_email():
            email1 = input("What is your email?: ")
            email2 = input("Type your email again: ")

            if email1 != email2:
                print("Emails don't match, try again.")
                confirm_email()
            elif email1 == email2:
                confirmed_email = email1
                return confirmed_email

        final_email = confirm_email()

        print(f"New User Created: First Name: {first_name}, "
              f"Last Name: {last_name}, Email: {final_email}\n"
              f"Adding New User to Google SpreadSheet...")

        user_manager = UserManager(
            first_name,
            last_name,
            final_email,
        )

        user_manager.upload_user()


start_here()


if __name__ == "__main__":
    start_here()
