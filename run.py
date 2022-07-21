'''Import gspread and Google OAuth modules'''
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

    return sales_data


def validate_data(values):
    """
    Convert string to Integers within the Try block
    Return ValueError if strings cannot be converted into Integers or if there
    aren't 6 values entered. The request loop will continue until valid data
    is supplied
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


def update_worksheet(data, sheet):
    """
    Add data to Google sheet
    """
    print(f'Adding {sheet} figures to worksheet')
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(data)
    print(f'{sheet} data added to spreadsheet!\n')


def calculate_surplus_stock(sales_row):
    """
    Compare sales with stock and calculate the surplus of each item

    the surplus is defined as the sales figures subtracted from the stock
    + positive surplus indicates waste
    - negative surplus indicates when stock was sold out
    """
    print('Calculating surlpus sandwiches now...')
    stock = SHEET.worksheet('stock').get_all_values()
    # stock_row = stock[len(stock)-1]
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    inputted_data = [int(num) for num in data]
    update_worksheet(inputted_data, 'sales')
    surplus_data = calculate_surplus_stock(inputted_data)
    update_worksheet(surplus_data, 'surplus')
  

main()
