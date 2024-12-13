import os
from dotenv import load_dotenv
from data.weather import Weather
from data.calendar import GoogleCal

def main(): 
    # load env variables for secret keys
    load_dotenv()
    weather_api_key = os.getenv('OPENWEATHER_API_KEY')

    weather = Weather(weather_api_key)
    calendar = GoogleCal()

    print(weather.fetch_weather("Denver"))
    print(calendar.fetch_calendar_events())

if __name__ == "__main__":
    main()