import os
from dotenv import load_dotenv
from data.weather import Weather
from data.calendar import GoogleCal
from PyQt5.QtWidgets import QApplication
from ui.display import MainWindow
import sys

CITY = "Denver"
def main(): 
    # load env variables for secret keys
    load_dotenv()
    weather_api_key = os.getenv('OPENWEATHER_API_KEY')

    weather = Weather(weather_api_key, CITY)
    calendar = GoogleCal()

    # print(weather.fetch_weather("Denver"))
    # print(calendar.fetch_calendar_events())

    # Create the application instance
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow(weather, calendar)
    window.show()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()