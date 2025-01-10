import datetime
from dotenv import load_dotenv
import logging
import json
import os
import requests

WEATHER_URL = "https://api.weatherapi.com/v1/forecast.json"
ICONS_FILE = "ui/icons.json"

class Weather:
    def __init__(self, city):

        self.logger = logging.getLogger(__name__)

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

        self.logger.info(f"Fetching weather for {self.city}")

        # Fetch weather data from OpenWeatherMap url passed in
        params = {
            "q": self.city,
            "key": self.api_key
        }
    
        try:
            response = requests.get(WEATHER_URL, params=params)
            response.raise_for_status()
            self.weather = response.json()
            if 'current' in self.weather and 'forecast' in self.weather:
                curr_weather = {
                    "temp": round(self.weather['current'].get('temp_f', 0)),
                    "condition": self.weather['current'].get('condition', {}).get('text', 'Unknown'),
                    "min" : round(self.weather['forecast']['forecastday'][0]['day'].get('mintemp_f', 0)),
                    "max" : round(self.weather['forecast']['forecastday'][0]['day'].get('maxtemp_f', 0)),
                    "rain_probability" : self.weather['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain', 0),
                    "moon_phase" : self.weather['forecast']['forecastday'][0]['astro'].get('moon_phase', 'Unknown')
                }
                return curr_weather
        except requests.exceptions.RequestException as reqerr:
            print(f"Error fetching weather data: {reqerr}")
        except requests.exceptions.ConnectionError as connerr: 
            print(f"Connection error: {connerr}") 
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
            icon = self.icons[f"{code}"]['day']
        else: 
            icon = self.icons[f"{code}"]['night']

        return f"ui/icons/{icon}"
