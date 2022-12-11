# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import sys # used for allowing user to exit the program

"""
Import datetime and date classes from datetime module
required to manipulate dates.
"""
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials
# pyfiglet module used to create logo for the app
import pyfiglet

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


def welcome_message():
    """
    Welcome message
    """
    logo = pyfiglet.figlet_format("     E l e g a n t\n           H a i r s t y l e s")
    print(logo)
    print("       Hello and welcome to Elegant Hairstyles appointment booking system!\n")
    print("================================================================================")


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
            print(f"Welcome back, {existing_user.value}!")
        else:
            print("Incorrect Username and Password combination\n")
    else:
        # username doesn't exist
        print("Incorrect Username and Password combination\n")


def get_date():
    """
    Function to get the preferred appointment date from user
    """
    print("\nPlease enter your preferred appointment date.")
    print("Date should be in YYYY-MM-DD format.")

    user_date_str = input("Enter date here: \n")
    validate_date(user_date_str)


def validate_date(date_str):
    """
    Function checks if date input by User matches the expected format
    and raises ValueError if it does not.
    """
    print("Hello from validate_date function")

    try:
        if date_str != datetime.strptime(date_str, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError()
    except ValueError:
        print("Invalid data: Date should be in YYYY-MM-DD format, please try again.\n")


get_date()


def login_register():
    """
    Function to check if User wants to Log In or Register.
    Checks if User input is a valid answer option.
    """
    print("Are you a returning Customer?\n")
    print("1 - Yes, I am a returning Customer and I want to Log In.")
    print("2 - No, I am a new Customer and I want to Register.")
    answer = input("Enter your answer option here: \n").strip()
    # repeat request for answer option until input provided is valid
    while answer not in ("1", "2"):
        print("You have entered an invalid value.")
        print("Please enter '1' or '2' to select your answer.\n")
        answer = input("Enter your answer option here: \n").strip()
    return answer


def main():
    """
    Displays welcome message and a menu containing two options to choose from.
    """
    welcome_message()

    print("\nPlease select from the following options by entering 1 or 2.\n")
    print("1 - Log In or Register for a free account.")
    print("2 - Exit the booking system.")

    answer = input("Enter your answer option here: \n").strip()

    if answer == "1":
        login_register()
    elif answer == "2":
        sys.exit("Thank you for using our booking system!")


main()
