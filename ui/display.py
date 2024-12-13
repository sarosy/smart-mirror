from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow, QListWidget
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
import sys

# Clock widget
class ClockWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 36px; color: white;")
        self.setAlignment(Qt.AlignCenter)
        self.update_time()

        # Timer to update clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        """Update the time display."""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.setText(current_time)

# Weather widget
class WeatherWidget(QWidget):
    def __init__(self, weather):
        super().__init__()

        self.weather = weather

        layout = QVBoxLayout()
        self.setLayout(layout)

        weather_label = QLabel("Today's weather:")
        layout.addWidget(weather_label)

        weather_now = QLabel(self.weather.fetch_weather())
        layout.addWidget(weather_now)


class CalendarWidget(QWidget):
    def __init__(self, calendar):
        super().__init__()

        self.calendar = calendar

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("This week's events:")
        label.setAlignment(Qt.AlignCenter)

        # Set the label as the central widget
        layout.addWidget(label)

        events = self.calendar.fetch_calendar_events()

        # Create a list widget for calendar events
        events_list = QListWidget()
        events_list.setAlternatingRowColors(True)
        events_list.setStyleSheet("background-color: #f9f9f9;")
        events_list.addItems(events)
        layout.addWidget(events_list)

class MainWindow(QMainWindow):
    def __init__(self, weather, calendar):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Hello World App")

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        
        # Create a QLabel widget
        label = QLabel("Hello, World!")

        # Set alignment for the label text
        label.setAlignment(Qt.AlignCenter)

        # Set the label as the central widget
        layout.addWidget(label)

        # Add Widgets
        weather_widget = WeatherWidget(weather)
        calendar_widget = CalendarWidget(calendar)

        layout.addWidget(weather_widget)
        layout.addWidget(calendar_widget)

        central_widget.setLayout(layout)


# Main Window
class SmartMirrorApp(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.setWindowTitle("Smart Mirror")
        self.setGeometry(100, 100, 800, 480)

        # Central widget and layout
        central_widget = QWidget(self)
        window = QWidget()
        window.setWindowTitle("My Application")

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Add Widgets
        # self.clock_widget = ClockWidget()
        # self.weather_widget = WeatherWidget(api_key, city="Denver")
        # self.calendar_widget = CalendarWidget()

        # self.layout.addWidget(self.clock_widget)
        # self.layout.addWidget(self.weather_widget)
        # self.layout.addWidget(self.calendar_widget)

        # Style the layout
        self.central_widget.setStyleSheet("background-color: black;")
        self.show()

        app = QApplication(sys.argv)

        # Create the main window widget
        window = QWidget()
        window.setWindowTitle("My Application")
        window.show()

        # Start the application's event loop
        app.exec_()
