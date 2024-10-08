import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    """Authenticate and return the Google Calendar service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def add_event_to_calendar(summary, description, start_time, end_time):
    """Add a new event to Google Calendar."""
    service = get_google_calendar_service()

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Amsterdam',  # Adjust to your time zone
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Amsterdam',  # Adjust to your time zone
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
