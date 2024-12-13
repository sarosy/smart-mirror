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
        # Mock function to fetch calendar events.
        return ["Meeting at 10 AM", "Lunch with Cam at 1 PM", "Gym at 6 PM"]