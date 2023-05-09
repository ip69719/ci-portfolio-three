# Imports to support application
import sys  # used for allowing user to exit the program
from datetime import datetime, date, timedelta  # required to manipulate dates
import calendar  # import calendar module used to get day of the week
import re  # required for email address validation
from tabulate import tabulate  # used to display the pandas df in a table style

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
bookings = SHEET.worksheet('bookings')
schedule = SHEET.worksheet('schedule')


class User:
    """
    A class used to represent a user
    Method written with help of my Mentor.

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
        future_appts = pd.DataFrame(columns=[
            'stylist', 'time slot', 'date', 'week day', 'customer'])
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
            print("Your future apopintment(s):\n")
            print(tabulate(
                future_appts, headers='keys', tablefmt='psql',
                showindex=False)
                )


def enter_email():
    """
    Function checks if an email input is valid and repeats request until
    an email address in a valid format is provided. The valid email address
    pattern is: username + @ symbol + domain name.

    The code was written with reference to the following GeeksforGeeks tutorial
    https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    new_user_email = input("\nPlease enter your email: \n")
    while not re.fullmatch(regex, new_user_email):
        print("\nPlease enter a valid email address.")
        print("Email address must have the following pattern:")
        print("username + @ symbol + domain name. Example: name@example.com")
        new_user_email = input("\nPlease enter your email: \n")

    return new_user_email


def get_username():
    """
    Function checks that username is not empty and
    repeats request until a valid username is provided.
    """
    username = input("\nPlease enter username: \n")
    while len(username.strip()) < 1:
        print("\nYou have entered an invalid username.")
        print("Username cannot be empty.")
        print("Please enter a username that is at least one character long.")
        username = input("\nPlease enter username: \n")
    return username


def get_password():
    """
    Function checks that password meets password requirements
    specified in validate password function and repeats the request
    until a valid password is provided.
    """
    while True:
        print("\nPlease enter a password that is at least 8 characters long.")
        print("It must contain at least 1 digit and 1 uppercase character.")
        password = input("\nPlease enter password: \n")
        if validate_password(password):
            break
    return password


def validate_password(password):
    """
    Function checks user password against the following conditions:
        - Password must be at least 8 characters long
        - Password must contain at least 1 digit
        - Password must have at least 1 uppercase character

    The results from this function are passed to get_password()

    Code was adopted from this Stack Overflow post:
    https://stackoverflow.com/questions/37794949/regular-expressions-for-password-in-python-3
    """
    try:
        if len(password) < 8:
            raise ValueError()
        if not any(c.isdigit() for c in password):
            raise ValueError()
        if not any(c.isupper() for c in password):
            raise ValueError()
        return True
    except ValueError:
        print("\nInvalid password, please try again.")
        return False


def welcome_message():
    """
    Welcome message
    """
    logo = pyfiglet.figlet_format("     E l e g a n t\n           H a i r s t y l e s")  # noqa:E501
    print(logo)
    print("         Hello and welcome to our appointment scheduling assistance app!\n")  # noqa:E501
    print("                You need to have an account to use this service.")
    print("================================================================================")  # noqa:E501


def register():
    """
    The function allows to register a new user. If user email already
    exists in the spreadsheet then the user is requested to login, otherwise
    new user details are collected.
    """
    new_user_email = enter_email()
    # Check if username exists
    existing_user = users.find(new_user_email, in_column=2)
    if existing_user:
        print("\n The email address you provided is already registered.")
        print("Please Log In")
        login()
    else:
        new_email = new_user_email
        new_username = get_username()
        new_user_pass = get_password()

    return [new_username, new_email, new_user_pass]


def add_new_user():
    """
    Function to insert new use record into spreadsheet
    """
    new_user = register()
    user_worksheet = SHEET.worksheet("users")
    user_worksheet.append_row(new_user)

    print("Registration complete!")

    user = User(new_user[0], new_user[1])
    main_authenticated_menu(user)


def login():
    """
    The function allows an existing user to login. Checks if user email
    matches to the record stored in the users worksheet.
    """
    email_input = enter_email()
    print("\nThank you. Please wait while we retrieve your details...\n")

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
        print("The email address you provided is not yet registered")
        print("Please register for free account")
        register()


def get_date():
    """
    Function to get the preferred appointment date from user
    """
    while True:
        print("\nPlease enter your preferred appointment date.")
        print("Date should be in YYYY-MM-DD format.")

        user_date_str = input("Enter date here: \n")
        if validate_date(user_date_str):
            break
    return user_date_str


def get_weekday(user_date_str):
    """
    Function to get day of the week from the user date input.

    Code written with reference to this tutorial:
    https://pynative.com/python-get-the-day-of-week/
    """
    # create date object in given format yyyy-mm-dd'
    user_date = datetime.strptime(user_date_str, "%Y-%m-%d")
    # to get name of day from date
    print('Day of Week for date selected is: ', calendar.day_name[user_date.weekday()])  # noqa:E501
    weekday = calendar.day_name[user_date.weekday()].lower()
    return weekday


def validate_date(date_str):
    """
    Function checks if date input by User matches the expected format, is a
    future date and raises ValueError if it does not.

    Adopted code from this Stack Overflow post to implement date validation:
    https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python

    """
    try:
        if date_str != datetime.strptime(date_str, "%Y-%m-%d").strftime('%Y-%m-%d'):  # noqa:E501
            raise ValueError()
        # Code to check that the date is in the future written by my Mentor
        date_entered = datetime.strptime(date_str, "%Y-%m-%d")
        todays_date = datetime.now()
        tomorrow = todays_date + timedelta(days=1)
        tomorrow_date_string = tomorrow.strptime(date_str, "%Y-%m-%d")
        if date_entered.date() < tomorrow.date():
            print(f"Please enter a future date: {tomorrow_date_string } or later")  # noqa:E501
            return False
        return True
    except ValueError:
        print("Invalid data: Date should be in YYYY-MM-DD format, please try again.\n")  # noqa:E501
        return False


def free_appt():
    """
    This function was written with help of my Mentor
    Malia Havlicek: https://github.com/maliahavlicek.

    The function collects data from the bookings spreadsheet and limits it
    to date selected by user.

    The function collects data from schedule spreadsheet and limits it
    to open time slots for day selected.

    The for loop within the function iterates over current schedule and appends
    rows with free time slots for day selected to an empty dataframe.
    The output is displayed to the user along with options to choose from.

    """
    user_date_str = get_date()
    day_selected = get_weekday(user_date_str)
    date_selected = user_date_str

    # get data from bookings spreadsheet
    bookings_all = pd.DataFrame(bookings.get_all_records())
    # limit data to date selected by user
    current_bookings = bookings_all.loc[bookings_all['date'] == date_selected]

    # get data from schedule spreadsheet
    schedule_all = pd.DataFrame(schedule.get_all_records())
    # limit it to the rows where the day of week column ==“open”
    current_schedule = schedule_all.loc[schedule_all[day_selected] == 'open']

    # create an empty pandas DataFrame
    available_appt = pd.DataFrame(
        columns=[
            'stylist', 'time slot',  'monday', 'tuesday',  'wednesday',
            'thursday', 'friday', 'saturday', 'sunday'])
    index = 0

    # the below code was written with help of my Mentor.
    for index, row in current_schedule.iterrows():
        available_stylist = row['stylist']
        available_time_slot = row['time slot']
        already_booked = current_bookings[
            (current_bookings['stylist'] == available_stylist) & (
                current_bookings['time slot'] == available_time_slot)]
        # returns all open appointments on the day
        if len(already_booked) == 0:
            available_appt.loc[index] = row.values
            index = index + 1
            available_time = available_appt[['stylist', 'time slot']]
    # if there are any free time slots for selected day
    if len(available_appt) > 0:
        print(f"\nWe have availability on {day_selected.capitalize()}, {user_date_str}!\n")  # noqa:E501
        print("Please call us to book an appointment: \n")
        print(tabulate(
            available_time, headers='keys', tablefmt='psql', showindex=False)
            )
    # if there are no free time slots for selected day
    else:
        print(f"\nUnfortunately we do not have any availability on {day_selected.capitalize()} {user_date_str}!\n")  # noqa:E501

    print("\nWould you like to choose a different day or exit?")
    print("Please select from the following options by entering 1 or 2.\n")
    print("1 - I would like to choose a different day.")
    print("2 - I would like to exit the system.")

    answer = check_user_answer()

    if answer == "1":
        free_appt()
    elif answer == "2":
        sys.exit("Thank you for using our appointments scheduling system!")


def main_authenticated_menu(user):
    """
    Function to recap user's apointments.
    Allows user to book an appointment or exit.
    """
    print(f"\nWelcome, {user.username}!")
    user.print_future_appointments()

    print("\nWould you like to book a new appointment?")
    print("Please select from the following options by entering 1 or 2.\n")
    print("1 - Yes, I want to book an appointment.")
    print("2 - No, I want to exit the booking system.")

    answer = check_user_answer()
    if answer == "1":
        free_appt()
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
    print("\nAre you a returning Customer?\n")
    print("1 - Yes, I am a returning Customer and I want to Log In.")
    print("2 - No, I am a new Customer and I want to Register.")

    answer = check_user_answer()
    if answer == "1":
        login()
    elif answer == "2":
        add_new_user()


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
