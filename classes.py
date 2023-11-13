import datetime
import requests
import json

class WeatherForecast:
    def __init__(self, location_key, api_key):
        self.location_key = location_key
        self.api_key = api_key
        self.weather_db = "weather_db.txt"
        self.weather_data = {}

    def __setitem__(self, date, weather): # allow you to set a weather forecast for a particular date.
        self.weather_data[date] = weather
        self._save_to_file(date, weather)

    def __getitem__(self, date): # allow you to get the weather forecast for a particular date.
        return self.weather_data.get(date, "Weather forecast not available for this date.")

    def __iter__(self): # allow you to iterate over all the dates for which the weather forecast is known.
        return iter(self.weather_data)

    def items(self): # return a generator of tuples in the format `(date, weather)` for already saved results.
        return ((date, self.weather_data[date]) for date in self.weather_data)

    def _save_to_file(self, date, precip_check): # Save to file "weather_db.txt"
        with open(self.weather_db, "a") as file:
            file.write("{};{};{}\n".format(str(date), self.location_key, precip_check))
        print(f"Saved to file: {date}, {self.location_key}, {precip_check}")

    def valid_date(self, enter_date): # To check if input an valid date
        try:
            datetime.datetime.strptime(enter_date, '%Y-%m-%d')
            return True
        except ValueError:
            print("Date entered is not valid.")
            return False

    def get_coordinates(self, location_input): # To get the coordinates from "http://www.mapquestapi.com/geocoding/v1/address"
        parameters = {
            "key": self.api_key,
            "location": location_input
        }
        response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params=parameters)
        data = json.loads(response.text)['results']
        lat = data[0]['locations'][0]['latLng']['lat']
        lng = data[0]['locations'][0]['latLng']['lng']
        return lat, lng

    def weather_req(self, lat, lng, weather_day): # To get the weather with the coordinates.
        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={weather_day}&end_date={weather_day}")
        weather_json = json.loads(weather.text)['daily']
        precipitation = float(weather_json['precipitation_sum'][0])
        return precipitation

    def precip_msg(self, precip_check): # To show messages if will rain or not.
        if precip_check > 0:
            print(f"It will rain, the precipitation is: {precip_check}")
        elif precip_check == 0:
            print("It will not rain.")
        else:
            print("I don't know.")

    def save_file(self, weather_day):
        lat, lng = self.get_coordinates(self.location_key)
        precip_check = self.weather_req(lat, lng, weather_day)
        self.precip_msg(precip_check)
        self.__setitem__(weather_day, precip_check)