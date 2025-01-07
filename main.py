from data.calendar import GoogleCal
from data.weather import Weather
from data.reminders import Reminders
from PyQt5.QtWidgets import QApplication
from ui.display import MainWindow
import sys

CITY = "Denver"
STYLE_SHEET="ui/stylesheet.qss"

def main(): 

    weather = Weather(CITY)
    calendar = GoogleCal()
    # reminders = Reminders()

    # Create the application instance
    app = QApplication(sys.argv)

    with open(STYLE_SHEET,"r") as f:
        app.setStyleSheet(f.read())

    # Create the main window
    window = MainWindow(weather, calendar)
    window.showFullScreen()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()