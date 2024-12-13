import requests
import json

class Weather:
    def __init__(self, api_key, city):
       self.api_key = api_key
       self.city = city

    def fetch_weather(self):
        """Fetch weather data from OpenWeatherMap API."""
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "imperial"  # Use "metric" for Celsius, "imperial" for Fahrenheit
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            weather = {
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize(),
                "city": data["name"]
            }
            return self.weather_string(weather)
        else:
            print("Failed to fetch weather data:", response.status_code)
            return None
        
    def weather_string(self, weather):
        return json.dumps(weather)
