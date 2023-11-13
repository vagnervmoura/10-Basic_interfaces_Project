"""
LINKs to search help:
To create a function valid_date: https://pt.stackoverflow.com/questions/377579/valida%C3%A7%C3%A3o-de-data-testes-com-python
To get LATITUDE and LONGITUDE: https://www.youtube.com/watch?v=tKy-IHAxt4s
To get the LOCATION and the KEY: https://developer.mapquest.com/user/me/profile
"""

from classes import WeatherForecast
import datetime

def get_user_date_option():
    return input("Insert the option do you prefer to check:\n"
                 " 1 - To check today\n"
                 " 2 - to check tomorrow\n"
                 " 3 - to check a specific day\n"
                 " 4 - to check some number of days in the future or past\n"
                 " 0 - To exit the program\n")


location_input = input("\nEnter the name of the city you want to get info about the weather:\n")
weather_forecast = WeatherForecast(api_key="k0bjBNdDAi6cjplDMbfKdTOuMqAPUT9V", location_key=location_input)

option = get_user_date_option()

if option == "0":
    print("\nThank you for using our system.\n\n")
    exit()
elif option == "1":
    weather_day = datetime.date.today()
    print("Today is: ", weather_day)
elif option == "2":
    weather_day = datetime.date.today() + datetime.timedelta(1)
    print("Tomorrow is: ", weather_day)
elif option == "3":
    enter_date = input("Enter the date in the following format 'YYYY-MM-DD':\n")
    while not weather_forecast.valid_date(enter_date):
        enter_date = input("Enter the date in the following format 'YYYY-MM-DD':\n")
    weather_day = datetime.datetime.strptime(enter_date, '%Y-%m-%d').date()
else:
    fut_or_pas = input("Choose the options:\n 1 - to the future\n 2 - to the past\n")
    if fut_or_pas == "1" or fut_or_pas == "2":
        check_day = int(input("How many days do you want to check from today:\n"))
        today = datetime.date.today()
        if fut_or_pas == "1":
            weather_day = today + datetime.timedelta(check_day)
        elif fut_or_pas == "2":
            weather_day = today - datetime.timedelta(check_day)
    else:
        print(f"Option {fut_or_pas} not available.\n\n")
        exit()

# Call save_file method to save weather information to the file
weather_forecast.save_file(weather_day)