import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Define the scopes your app needs
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# File for storing credentials
CREDENTIALS_FILE = 'gcal_credentials.json'

class GoogleCal:
    def __init__(self):
        self.creds = self.authenticate_google_account()

    def authenticate_google_account(self):
        creds = None
        # Check if the token.json file exists, which stores user credentials
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as token:
                try:
                    creds_data = json.load(token)
                    if isinstance(creds_data, dict):  # Ensure it's a dictionary
                        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
                    else:
                        print("Error: creds_data is not a valid dictionary")
                        creds = None
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    creds = None
                except ValueError as e:
                    print(f"Error loading credentials: {e}")
                    creds = None
                
        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials to a file (using JSON)
            with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as token:
                token_data = creds.to_json()  # Get credentials as JSON
                creds_dict = json.loads(token_data)
                json.dumps(creds_dict, token)  # Save the dictionary to file

        return creds
    

    def fetch_calendar_events(self):

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # List all calendars the user has access to
            calendar_list = service.calendarList().list().execute()

            enabled_calendars = []

            for calendar in calendar_list['items']:
                # Check if the calendar is selected (enabled)
                if calendar.get('selected', True):
                    enabled_calendars.append(calendar)

            all_events = []

            now = datetime.datetime.now(datetime.timezone.utc)
            timedelta = datetime.timedelta(days=7)
            week_end = now + timedelta
            time_min = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            time_max = week_end.strftime('%Y-%m-%dT%H:%M:%SZ')

            for calendar in enabled_calendars:
                events_result = service.events().list(
                    calendarId=calendar['id'],
                    timeMin=time_min,
                    timeMax=time_max,
                    maxResults=5,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()

                events = events_result.get('items', [])
                all_events.extend(events)

            if not all_events:
                print("No upcoming events found in any calendars.")
            else:
                print("Upcoming events from all calendars:")
                for event in all_events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(f"{start}: {event['summary']}")

        
        except Exception as e:
            print(f"An error occurred: {e}")

