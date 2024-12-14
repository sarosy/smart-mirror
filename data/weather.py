import datetime
from dotenv import load_dotenv
import json
import os
import requests

WEATHER_URL = "https://api.weatherapi.com/v1/forecast.json"
ICONS_FILE = "ui/icons.json"

class Weather:
    def __init__(self, city):

        # load env variables for secret keys
        load_dotenv()
        api_key = os.getenv('WEATHER_API_KEY')
        self.api_key = api_key

        self.city = city
        self.timezone = datetime.datetime.now().astimezone().tzinfo
        self.weather = None
        with open(ICONS_FILE, 'r', encoding='utf-8') as f:
            self.icons = json.load(f)

    def fetch_weather(self):

        # Fetch weather data from OpenWeatherMap url passed in
        params = {
            "q": self.city,
            "key": self.api_key
        }
        response = requests.get(WEATHER_URL, params=params)
        if response.status_code == 200:
            self.weather = response.json()
            curr_weather = {
                "temp": round(self.weather['current']['temp_f']),
                "condition": self.weather['current']['condition']['text'],
                "min" : round(self.weather['forecast']['forecastday'][0]['day']['mintemp_f']),
                "max" : round(self.weather['forecast']['forecastday'][0]['day']['maxtemp_f']),
                "rain_probability" : self.weather['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
                "moon_phase" : self.weather['forecast']['forecastday'][0]['astro']['moon_phase']
            }
            return weather_string(curr_weather)
        else:
            print(f"Failed to fetch weather data: {response.status_code}")
            return None
    
    def get_icon(self):
        # Get the code for the current weather conditions
        code = self.weather['current']['condition']['code']

        # Get the time of sunset and the current time
        sunset = self.weather['forecast']['forecastday'][0]['astro']['sunset']
        sunset_dt = datetime.datetime.strptime(sunset, "%I:%M %p").time()
        now = datetime.datetime.now(self.timezone).time()

        # Check if the sun has set to get appropriate icon
        if (now < sunset_dt):
            pass
            icon = self.icons[f"{code}"]['day']
        else: 
            icon = self.icons[f"{code}"]['night']

        return f"ui/icons/{icon}"

        
def weather_string(weather):
    return json.dumps(weather)
