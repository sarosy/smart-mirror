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

logger = logging.getLogger(__name__)

class GoogleCal:
    def __init__(self):
        self.creds = self.authenticate_google_account()

    def authenticate_google_account(self):
        # load env variables for token and key file locations
        load_dotenv()
        token_file = os.getenv('GOOGLE_TOKEN_FILE')
        secret_file = os.getenv('GOOGLE_SECRET_FILE')
    
        creds = self.load_credentials(token_file)

        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    creds= self.authorization_flow(secret_file)
            elif not creds or not creds.refresh_token:
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
                        logger.error("Error: creds_data is not a valid dictionary")
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON: {e}")
                except ValueError as e:
                    logger.error(f"Error loading credentials: {e}")
        return creds

    def save_credentials(self, creds, token_file):
        with open(token_file, 'w', encoding='utf-8') as token:
            token_data = creds.to_json()
            creds_dict = json.loads(token_data)
            json.dump(creds_dict, token)
    

    def fetch_calendar_events(self, start_date):

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

            timedelta = datetime.timedelta(hours=23, minutes=59)
            end_date = start_date + timedelta
            time_min = start_date.strftime(GOOGLE_DATE_QUERY_FORMAT)
            time_max = end_date.strftime(GOOGLE_DATE_QUERY_FORMAT)
            
            for calendar in enabled_calendars:
                try:
                    events_result = service.events().list(
                        calendarId=calendar['id'],
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()

                    events = events_result.get('items', [])
                    all_events.extend(events)
                except HttpError as http_err:
                    logger.error(f"HTTP error occurred: {http_err}")
                    return []
                except Exception as e:
                    logger.error(f"An unexpected error occurred: {e}")
                    return []

            if not all_events:
                logger.info(f"No events from {time_min} to {time_max} found in any calendars.")
                return []
            
            
            # Convert start date or datetime to a datetime object
            def get_event_datetime(event, start):

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

            event_summaries = []
            for event in all_events:
                start = get_event_datetime(event, start=True)
                end = get_event_datetime(event, start=False)
                summary = event['summary']
                event_summaries.append({
                    'start': start,
                    'end': end,
                    'summary' : summary,
                    })
                
            # Sort events by start datetime
            sorted_events = sorted(event_summaries, key=lambda event: event['start'])
            return sorted_events

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return []

