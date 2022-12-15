"""
Imports to support application
"""

import sys  # used for allowing user to exit the program
from datetime import datetime, date  # required to manipulate dates
import calendar  # import calendar module

# makes sheets dataobjects that are easier to search/manipulate
import pandas as pd

import gspread
from google.oauth2.service_account import Credentials

import pyfiglet  # module used to create logo for the app

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('elegant_hairstyles')

users = SHEET.worksheet('users')


class User:
    """
    A class used to represent a user

    ...
    Attributes
    ----------
    user_name = str
        the customer's username
    email = str
        the customer's email (unique to system)

    Methods
    --------
    print_future_appointments
        Return the customer future appointments
    """

    def __init__(self, username, email):
        """
        Instance attributes
        """
        self.username = username
        self.email = email

    def print_future_appointments(self):
        """
        Method to return list of future apointments.
        """
        # get date from bookings spreadsheet
        worksheet = SHEET.worksheet('bookings')
        # convert into DataFrame and filter records for specific user
        all_data = pd.DataFrame(worksheet.get_all_records())
        appointments = all_data.loc[all_data['customer'] == self.email]

        todays_date = date.today()
        # create an empty pandas DataFrame
        future_appts = pd.DataFrame(columns=['stylist', 'time slot', 'date', 'week day', 'customer']) 
        index = 0
        # iterate through each row and append rows to the new DataFrame
        for index, row in appointments.iterrows():
            appointment_date = datetime.strptime(row['date'], "%Y-%m-%d")
            if appointment_date.date() >= todays_date:
                future_appts.loc[index] = row.values
                index = index + 1
        # print future appointements
        if len(future_appts) < 1:
            print("You have no future apopintments at this time.\n")
        else:
            print("Your future apopintment(s).\n")
            print(future_appts)


def welcome_message():
    """
    Welcome message
    """
    logo = pyfiglet.figlet_format("     E l e g a n t\n           H a i r s t y l e s")
    print(logo)
    print("       Hello and welcome to Elegant Hairstyles appointment booking system!\n")
    print("================================================================================")


def register():
    """
    The function allows to register a new user. If user email already
    exists in the spreadsheet then the user is requested to login, otherwise
    new user details are collected. 
    """
    new_user_email = input("Please enter your email: \n")
    # Check if username exists
    existing_user = users.find(new_user_email, in_column=2)
    if existing_user:
        print("The email address you provided is already registered")
        print("Please Log In")
        login()
    else:
        new_email = new_user_email
        new_username = input("Please enter username: \n")
        new_user_pass = input("Please enter password: \n")

    return [new_email, new_username, new_user_pass]


def login():
    """
    The function allows an existing user to login. Checks if user email
    matches to the record stored in the users worksheet.
    """
    email_input = input("\nPlease enter your email: ")
    print("Thank you. Please wait while we retrieve your details...")

    # Check if username exists
    existing_user = users.find(email_input, in_column=2)

    if existing_user:
        # Get row number in which username is found
        row_user = existing_user.row
        # Get existing user details
        user_details = users.row_values(row_user)
        # check password
        username_password_input = input("Please enter your password: \n")
        if username_password_input == user_details[2]:
            user = User(user_details[0], user_details[1])
            main_authenticated_menu(user)
        else:
            print("Incorrect Username and Password combination\n")
            login()
    else:
        # username doesn't exist
        print("Incorrect Username and Password combination\n")
        login()


def get_weekday():
    """
    Get day of the week from the user input date
    """
    user_date_str = get_date()
    # create date object in given format yyyy-mm-dd'
    user_date = datetime.strptime(user_date_str, "%Y-%m-%d")
    # to get name of day from date
    print('Day of Week (str): ', calendar.day_name[user_date.weekday()])
    weekday = calendar.day_name[user_date.weekday()]
    print(weekday)


def get_date():
    """
    Function to get the preferred appointment date from user
    """
    print("\nPlease enter your preferred appointment date.")
    print("Date should be in YYYY-MM-DD format.")

    user_date_str = input("Enter date here: \n")
    validate_date(user_date_str)
    if not validate_date(user_date_str):
        get_date()
    return user_date_str


def validate_date(date_str):
    """
    Function checks if date input by User matches the expected format
    and raises ValueError if it does not.
    """
    print("Hello from validate_date function")

    try:
        if date_str != datetime.strptime(date_str, "%Y-%m-%d").strftime('%Y-%m-%d'):  # noqa:E501
            raise ValueError()
        return True
    except ValueError:
        print("Invalid data: Date should be in YYYY-MM-DD format, please try again.\n")  # noqa:E501
        return False


def main_authenticated_menu(user):
    """
    Function to recap user's apointments.
    Allows user to book an appointment or exit.
    """
    print(f"Welcome back, {user.username}!")
    user.print_future_appointments()

    print("\nWould you like to book a new appointment?\n")
    print("Please select from the following options by entering 1 or 2.\n")
    print("1 - Yes, I want to book an appointment.")
    print("2 - No, I want to exit the booking system.")

    answer = check_user_answer()
    if answer == "1":
        print("book new appointment")
        get_date()
    elif answer == "2":
        sys.exit("Thank you for using our booking system!")


# Code to help standardise user input written by my Mentor
def check_user_answer():
    """
    Helper function to check if user answer is valid.
    The loop will repeatedly request user to re-enter answer option,
    until a valid answer is provided.

    """
    answer = input("Enter your answer option here:\n").strip()
    while answer not in ("1", "2"):
        print("\nYou have entered an invalid value.")
        print("Please enter '1' or '2' to select your answer.")
        answer = input("Enter your answer option here:").strip()
    return answer


def login_register():
    """
    Function to check if User wants to Log In or Register.
    Checks if User input is a valid answer option.
    """
    print("Are you a returning Customer?\n")
    print("1 - Yes, I am a returning Customer and I want to Log In.")
    print("2 - No, I am a new Customer and I want to Register.")

    answer = check_user_answer()
    if answer == "1":
        login()
    elif answer == "2":
        register()


def main():
    """
    Displays welcome message and a menu containing two options to choose from.
    """
    welcome_message()

    print("\nPlease select from the following options by entering 1 or 2.\n")
    print("1 - Log In or Register for a free account.")
    print("2 - Exit the booking system.")

    answer = check_user_answer()

    if answer == "1":
        login_register()
    elif answer == "2":
        sys.exit("Thank you for using our booking system!")


main()
