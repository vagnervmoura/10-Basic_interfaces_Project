import datetime

import requests
import pprint
import sys
from datetime import datetime, timedelta, date

def valid_date():
    try:
        datetime.strptime(enter_date, '%Y-%m-%d')
        print(f"Date entered: {enter_date}")
        return True
    except ValueError:
        print("Date entered is not valid.")
        return False


option = input("Insert the option do you prefer to check:\n"
               " 1 - To check today\n"
               " 2 - to check tomorow\n"
               " 3 - to check an specific day\n"
               " 4 - to check some number of days in the future or past\n")
if option == "1":
    print("Today is: ", date.today())

elif option == "2":
    tomorrow = date.today() + timedelta(1)
    print("Tomorrow is: ", tomorrow.strftime('%Y-%m-%d'))

elif option == "3":
    enter_date = input("Enter the date in the following format: 'YYYY-MM-DD':\n")
    valid_date()


elif option == "4":
    fut_or_pas = input("Choose the options:\n 1 - to future\n 2 - to past?\n")
    if (fut_or_pas == "1") or (fut_or_pas == "2"):
        check_day = int(input("How many days do you want to check from today:\n"))
        today = date.today()
        if fut_or_pas == "1":
            fut = date.fromordinal(today.toordinal() + check_day)
            print(f"The future day is: {fut}")
        elif fut_or_pas == "2":
            past = date.fromordinal(today.toordinal() - check_day)
            print(f"The past day is: {past}")
    else:
        print("No option available.")