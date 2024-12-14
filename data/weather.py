import requests
import json

# CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
# DAILY_WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"

WEATHER_URL = "https://api.weatherapi.com/v1/forecast.json"

class Weather:
    def __init__(self, api_key, city):
       self.api_key = api_key
       self.city = city

    def fetch_weather(self):

        # Fetch weather data from OpenWeatherMap url passed in
        params = {
            "q": self.city,
            "key": self.api_key
        }
        response = requests.get(WEATHER_URL, params=params)
        if response.status_code == 200:
            weather = response.json()
            curr_weather = {
                "temp": round(weather['current']['temp_f']),
                "condition": weather['current']['condition']['text'],
                "min" : round(weather['forecast']['forecastday'][0]['day']['mintemp_f']),
                "max" : round(weather['forecast']['forecastday'][0]['day']['maxtemp_f']),
                "rain_probability" : weather['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
                "moon_phase" : weather['forecast']['forecastday'][0]['astro']['moon_phase']
            }
            return weather_string(curr_weather)
        else:
            print(f"Failed to fetch weather data: {response.status_code}")
            return None
        
def weather_string(weather):
    return json.dumps(weather)
