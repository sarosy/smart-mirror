from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout,QGridLayout, QWidget, QMainWindow, QListWidget, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import datetime
import sys

# Clock widget
class ClockWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 36px; color: white;")
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.update_time()

        # Timer to update clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        """Update the time display."""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.setText(current_time)

# Weather widget
class WeatherWidget(QWidget):
    def __init__(self, weather):
        super().__init__()

        self.weather = weather

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Fetching current weather and creating label
        weather_now = self.weather.fetch_weather()
        
        # Getting icon for current conditions and loading image
        icon = self.weather.get_icon()
        pixmap = QPixmap(icon)
        
        degree_sign = "\u00B0"
        temp = f"{weather_now['temp']}{degree_sign}F" 
        min = f"{weather_now['min']}{degree_sign}F" 
        max = f"{weather_now['max']}{degree_sign}F"

        # Create a horizontal layout for the icon and temperature
        daily_temp_layout = QHBoxLayout()
        
        min_label = QLabel(min)
        max_label = QLabel(max)

        min_label.setStyleSheet("font-size: 20px; color: white;")
        max_label.setStyleSheet("font-size: 20px; color: white;")

        min_label.setAlignment(Qt.AlignLeft)
        max_label.setAlignment(Qt.AlignRight)

        daily_temp_layout.addWidget(min_label)
        daily_temp_layout.addWidget(max_label)

        # Create a horizontal layout for the icon and current temperature
        current_weather_layout = QHBoxLayout()

        # Creating label for icon
        icon_label = QLabel()

        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        icon_label.setPixmap(scaled_pixmap)

        temp_label = QLabel(str(temp))
        temp_label.setAlignment(Qt.AlignBottom)
        temp_label.setStyleSheet("font-size: 36px; color: white;")

        current_weather_layout.addWidget(icon_label)
        current_weather_layout.addWidget(temp_label)

        main_layout.addLayout(daily_temp_layout)
        main_layout.addLayout(current_weather_layout)


class CalendarWidget(QWidget):
    def __init__(self, calendar):
        super().__init__()

        self.calendar = calendar

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        label = QLabel("This week's events:")
        label.setStyleSheet("font-size: 36px; color: white;")
        label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(label)

        weekly_schedule = QHBoxLayout()

        # Get the start of the current day as a UTC datetime
        start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date_utc = start_date.astimezone(datetime.timezone.utc)
        
        # Get events for each of the next 7 days and add them to the weekly schedule
        for i in range(7):

            # Create label for the day
            day_layout = QVBoxLayout()
            day_str = start_date_utc.strftime("%a, %b %d")
            day_label = QLabel(day_str)
            label.setStyleSheet("font-size: 20px; color: white;")
            day_layout.addWidget(day_label)
            
            # Get events for that day
            events = self.calendar.fetch_calendar_events(start_date_utc)

            # Get relevant event information to display
            event_summaries = []
            for event in events:
                event_summaries.append(f"{event['start'].strftime('%I:%M %p')} - {event['end'].strftime('%I:%M %p')}: {event['summary']}")

            if not event_summaries:
                event_summaries.append("No events scheduled for today.")

            # Add event summaries
            events_list = QListWidget()
            events_list.addItems(event_summaries)
            day_layout.addWidget(events_list)
            weekly_schedule.addLayout(day_layout)

            timedelta = datetime.timedelta(days=1)
            start_date_utc += timedelta

        main_layout.addLayout(weekly_schedule)
        
class MainWindow(QMainWindow):
    def __init__(self, weather, calendar):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Smart Mirror")
        self.setGeometry(100, 100, 800, 480)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # left, top, right, bottom
        layout.setSpacing(5)  # space between widgets


        # Add Widgets
        clock_widget = ClockWidget()
        weather_widget = WeatherWidget(weather)
        calendar_widget = CalendarWidget(calendar)
        
        clock_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add widgets to specific positions in the grid (row, column, row span, column span)
        layout.addWidget(clock_widget, 2, 1, 1, 1, Qt.AlignBottom | Qt.AlignRight)  # Bottom right corner
        layout.addWidget(calendar_widget, 0, 0, 1, 2)  # Top row, spanning two columns
        layout.addWidget(weather_widget, 2, 0, 1, 1, Qt.AlignBottom | Qt.AlignLeft)  # Bottom left corner

        central_widget.setLayout(layout)
