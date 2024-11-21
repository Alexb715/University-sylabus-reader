# Import required libraries for datetime, file operations, and Google API
from datetime import datetime
import os.path
from parser import parseTest as pdf  # Importing the PDF parsing module (assumes it extracts dates and titles)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the required API scopes for interacting with Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]
timeZone = 'America/Halifax'  # The time zone for the events to be created

# Class to interact with the Google Calendar API
class GoogleCalendarAPI:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        """Initialize the GoogleCalendarAPI class with file paths for credentials and token."""
        self.credentials_file = credentials_file  # Path to the credentials file
        self.token_file = token_file  # Path to the token file (stores the OAuth2 credentials)
        self.creds = None  # Variable to store credentials
        self.service = None  # Variable to store the Google Calendar service object
    
    def load_credentials(self):
        """Load the user's credentials from the token file or authenticate the user."""
        if os.path.exists(self.token_file):
            # Load the existing credentials from token.json if it exists
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials exist, we need to authenticate the user
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired credentials using the refresh token
                self.creds.refresh(Request())
            else:
                # Authenticate the user if no valid credentials exist
                self._authenticate_user()
            # Save the credentials for future use
            self._save_credentials()
    
    def _authenticate_user(self):
        """Handle the OAuth2 authentication process."""
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
        self.creds = flow.run_local_server(port=0)  # Launch the OAuth flow in a local server
    
    def _save_credentials(self):
        """Save the credentials to the token file to reuse in the future."""
        with open(self.token_file, "w") as token:
            token.write(self.creds.to_json())  # Write the credentials to token.json
    
    def build_service(self):
        """Build the Google Calendar service object."""
        if self.creds is None:
            raise ValueError("Credentials not loaded. Call load_credentials first.")
        
        # Use the loaded credentials to build the Calendar API service object
        self.service = build("calendar", "v3", credentials=self.creds)
    
    def CreateEvent(self, date, title):
        """Create a Google Calendar event based on the provided date and title."""
        try:
            # Convert the date from 'DD-MM-YYYY' format to 'YYYY-MM-DD' format
            formatted_date = datetime.strptime(date, '%d-%m-%Y').date()
            formatted_date = formatted_date.strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date format, please use 'DD-MM-YYYY'.")
            return
        
        # Define the event details
        event = {
            'summary': title,  # The title of the event (e.g., the test name)
            'start': {
                'date': formatted_date,  # Start date (same as the end date)
                'timeZone': timeZone,  # Time zone for the event
            },
            'end': {
                'date': formatted_date,  # End date (same as the start date)
                'timeZone': timeZone,  # Time zone for the event
            },
            'reminders': {
                'useDefault': True,  # Use default reminders (e.g., 10 minutes before the event)
            },
        }
        
        # Insert the event into the user's primary calendar
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))  # Print the link to the created event

# Instantiate the GoogleCalendarAPI class
google = GoogleCalendarAPI()

# Load credentials and build the Google Calendar service
google.load_credentials()
google.build_service()

# Ask the user to provide the location of the PDF file
print('input pdf location')
location = input()  # User inputs the path to the PDF file

# Parse the provided PDF to extract test dates and titles
data = pdf  # This uses the parseTest class from the parser module
data.get(location)  # Assuming this extracts the necessary data (dates and titles)

# Loop through the extracted dates and titles to create Google Calendar events
for i in range(len(data.dates)):
    google.CreateEvent(data.dates[i], data.title[i])  # Create an event for each test date and title
