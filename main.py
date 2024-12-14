import os
from dotenv import load_dotenv
from data.weather import Weather
from data.calendar import GoogleCal
from PyQt5.QtWidgets import QApplication
from ui.display import MainWindow
import sys
from data.location import CITY

STYLE_SHEET="ui/stylesheet.qss"

def main(): 
    # load env variables for secret keys
    load_dotenv()
    weather_api_key = os.getenv('WEATHER_API_KEY')

    weather = Weather(weather_api_key, CITY)
    calendar = GoogleCal()

    # Create the application instance
    app = QApplication(sys.argv)

    with open(STYLE_SHEET,"r") as f:
        app.setStyleSheet(f.read())

    # Create the main window
    window = MainWindow(weather, calendar)
    window.show()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()