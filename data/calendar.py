import logging
from googleapiclient.errors import HttpError
import datetime
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

# Define the scopes your app needs
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

GOOGLE_DATE_QUERY_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class GoogleCal:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.creds = self.authenticate_google_account()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def authenticate_google_account(self):
        # load env variables for token and key file locations
        load_dotenv()
        token_file = os.getenv('GOOGLE_TOKEN_FILE')
        secret_file = os.getenv('GOOGLE_SECRET_FILE')
    
        self.logger.info(f"Loading credentials from {token_file}")
        creds = self.load_credentials(token_file)

        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            self.logger.info("No valid credentials found")
            if creds and creds.expired and creds.refresh_token:
                try:
                    self.logger.info("Refreshing credentials")
                    creds.refresh(Request())
                except RefreshError as e:
                    self.logger.error(f"Error refreshing credentials: {e}")
                    creds= self.authorization_flow(secret_file)
            elif not creds or not creds.refresh_token:
                self.logger.info("No refresh token found, starting authorization flow")
                creds= self.authorization_flow(secret_file)

            self.save_credentials(creds, token_file)

        return creds
    
    def authorization_flow(self, secret_file):
        flow = InstalledAppFlow.from_client_secrets_file(
            secret_file, SCOPES)
        creds = flow.run_local_server(port=0, access_type='offline')
        return creds

    def load_credentials(self, token_file):
        creds = None
        if os.path.exists(token_file):
            with open(token_file, 'r', encoding='utf-8') as token:
                try:
                    creds_data = json.load(token)
                    if isinstance(creds_data, dict):
                        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
                    else:
                        self.logger.error("Error: creds_data is not a valid dictionary")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON: {e}")
                except ValueError as e:
                    self.logger.error(f"Error loading credentials: {e}")
        return creds

    def save_credentials(self, creds, token_file):
        self.logger.info(f"Saving credentials to {token_file}")
        with open(token_file, 'w', encoding='utf-8') as token:
            token_data = creds.to_json()
            creds_dict = json.loads(token_data)
            json.dump(creds_dict, token)
    

    def fetch_calendar_events(self, start_date):
        self.logger.info(f"Fetching events for {start_date}")
        enabled_calendars = self.get_enabled_calendars()
        all_events = self.get_events_for_calendars(enabled_calendars, start_date)
        return all_events

    def get_enabled_calendars(self):
        self.logger.info("Fetching enabled calendars")
        calendar_list = self.service.calendarList().list().execute()
        return [calendar for calendar in calendar_list['items'] if calendar.get('selected', True)]

    def get_events_for_calendars(self, calendars, start_date):
        self.logger.info(f"Fetching events for {len(calendars)} calendars")

        all_events = []
        timedelta = datetime.timedelta(hours=23, minutes=59)
        end_date = start_date + timedelta
        time_min = start_date.strftime(GOOGLE_DATE_QUERY_FORMAT)
        time_max = end_date.strftime(GOOGLE_DATE_QUERY_FORMAT)
        for calendar in calendars:
            try:
                events_result = self.service.events().list(
                    calendarId=calendar['id'],
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                all_events.extend(events_result.get('items', []))
            except HttpError as http_err:
                self.logger.error(f"HTTP error occurred: {http_err}")
                return []
            except Exception as e:
                self.logger.error(f"Error: {e}")
                return []
        return self.process_events(all_events)

    def process_events(self, events):
        event_summaries = []
        for event in events:
            start = self.get_event_datetime(event, start=True)
            end = self.get_event_datetime(event, start=False)
            summary = event['summary']
            event_summaries.append({
                'start': start,
                'end': end,
                'summary': summary,
            })
        return sorted(event_summaries, key=lambda event: event['start'])

    def get_event_datetime(self, event, start):
        time_key = 'start' if start else 'end'
        # TODO deal with time zones on events
        if 'dateTime' in event[time_key]:
            # If 'dateTime' is present, use it
            start = event[time_key]['dateTime']
            return datetime.datetime.fromisoformat(start)
        elif 'date' in event[time_key]:
            # If only 'date' is present, assume the start of the day
            start = event[time_key]['date']
            return datetime.datetime.fromisoformat(start).replace(tzinfo=datetime.timezone.utc)
        else:
            # Handle unexpected cases where neither 'dateTime' nor 'date' is present
            raise ValueError(f"Event {time_key} time is missing.")

