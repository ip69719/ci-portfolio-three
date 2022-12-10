# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

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


def login():
    """
    The function allows an existing user to login. Checks if user email
    matches to the record stored in the users worksheet.
    """
    email_input = input("\nPlease enter your email: ")
    print("Thank you. Please wait while we retrieve your details...")

    # Check if username exists
    existing_user = users.find(email_input)

    if existing_user:
        print('user found')
    else:
        print('user not found')


login()


def get_date():
    """
    Function to get the preferred appointment date from user
    """
    print("\nPlease enter your preferred appointment date.")
    print("Date should be in YYYY-MM-DD format.")

    user_date_str = input("Enter date here: ")
    print(user_date_str)


get_date()
