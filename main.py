"""
LINKs to search help:
To create a function valid_date: https://pt.stackoverflow.com/questions/377579/valida%C3%A7%C3%A3o-de-data-testes-com-python
To get LATITUDE and LONGITUDE: https://www.youtube.com/watch?v=tKy-IHAxt4s
To get the LOCATION and the KEY: https://developer.mapquest.com/user/me/profile
"""

import datetime
from datetime import datetime, timedelta, date
import requests
import json

weather_db="weather_db.txt"
option = None
location_input = input("\n\nEnter the name of City you want to get info about the weather:\n")



### TO GET LATITUDE AND LONGITUDE
parameters = {
    "key" : "k0bjBNdDAi6cjplDMbfKdTOuMqAPUT9V",
    "location" : location_input
}
response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params=parameters)
data = json.loads(response.text)['results']
lat = data[0]['locations'][0]['latLng']['lat']
lng = data[0]['locations'][0]['latLng']['lng']
# print(lat, lng)

def valid_date():
    try:
        datetime.strptime(enter_date, '%Y-%m-%d')
        weather_day = str(enter_date)
        print(f"Date entered: {weather_day}")
        return True
    except ValueError:
        print("Date entered is not valid.")
        return False

option = int(input("Insert the option do you prefer to check:\n"
               " 1 - To check today\n"
               " 2 - to check tomorow\n"
               " 3 - to check an specific day\n"
               " 4 - to check some number of days in the future or past\n"
               " 0 - To exit the program\n"))

if option == 0:
    print("\nThank you for using our system.\n\n")
    exit()

elif option == 1:
    weather_day = date.today()
    print("Today is: ", weather_day)

elif option == 2:
    weather_day = date.today() + timedelta(1)
    print("Tomorrow is: ", weather_day)

elif option == 3:
    enter_date = str(input("Enter the date in the following format: 'YYYY-MM-DD':\n"))
    valid_date()

elif option == 4:
    fut_or_pas = input("Choose the options:\n 1 - to future\n 2 - to past?\n")
    if (fut_or_pas == "1") or (fut_or_pas == "2"):
        check_day = int(input("How many days do you want to check from today:\n"))
        today = date.today()
        if fut_or_pas == "1":
            weather_day = date.fromordinal(today.toordinal() + check_day)
            print(f"The future day is: {weather_day}")
        elif fut_or_pas == "2":
            weather_day = date.fromordinal(today.toordinal() - check_day)
            print(f"The past day is: {weather_day}")
    else:
        print(f"Option {fut_or_pas} not available.\n\n")

else:
    print(f"Option {option} not available.\n\n")

def weather_req():
    weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={weather_day}&end_date={weather_day}")
    weather_json = json.loads(weather.text)['daily']
    precipitation = float(weather_json['precipitation_sum'][0])
    precip_check = precipitation
    return precip_check
precip_check = weather_req()



def precip_msg(precip_check):
    if precip_check > 0:
        print(f"It will rain, the precipitation is: {precip_check}")
    #    precip_msg = str(f"It will rain, the precipitation is: {precipitation}")
    elif precip_check == 0:
        print("It wil not rain.")
    #    precip_msg = str("It wil not rain.")
    else:
        print("I don't know.")
    #    precip_msg = str("I don't know.")


def save_file():
    #        weather_day, location_input, precipitation = row.strip().split(";")

    with open(weather_db, "a") as file:  # To create a new weather_db.txt in case not already exist on folder.
        pass

    weather_dic = {}
    write_db = True
    with open(weather_db, "r") as file:
        for row in file:
            w_day, l_input, precip = row.strip().split(";")
#            print(w_day, l_input, precip)
            weather_dic[w_day] = {
                "l_input": l_input,
                "precip": precip
            }

            if (str(w_day)) == (str(weather_day)):
                if (str(l_input)) == (str(location_input)):
                    write_db = False
                    precip_check = float(precip)
                    precip_msg(precip_check)
                    break
            else:
                write_db = True

    if write_db == True:
        weather_req()
        precip_check = weather_req()
        precip_msg(precip_check)
        with open(weather_db, "a") as file:
            file.write("{};{};{}\n".format(weather_day, location_input, precip_check))
        file.close()

save_file()