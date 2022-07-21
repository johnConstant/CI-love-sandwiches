'''Import gspread and Google OAuth modules'''
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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from user
    """
    while True:
        print('\nPlease enter sales data from the last market')
        print('Data should be 6 numbers, separated by commas')
        print('Example: 1,2,3,4,5,6 \n')

        data_str = input("Enter your sales figures here:")

        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid!')
            break


def validate_data(values):
    """
    Convert string to Integers within the Try block
    Return ValueError if strings cannot be converted into Integers
    Or if there aren't 6 values entered
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required. You only entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")
        return False
    
    return True


get_sales_data()
