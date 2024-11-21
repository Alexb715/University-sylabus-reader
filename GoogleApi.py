import datetime
import os.path
from parser import parseTest as pdf
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
timeZone = 'America/Halifax'
class GoogleCalendarAPI:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.service = None
    
    def load_credentials(self):
        """Load the user's credentials from the token file or perform authentication."""
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials exist, authenticate the user
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self._authenticate_user()
            # Save the credentials for the next run
            self._save_credentials()
    
    def _authenticate_user(self):
        """Authenticate the user by running the OAuth flow."""
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
        self.creds = flow.run_local_server(port=0)
    
    def _save_credentials(self):
        """Save the credentials to the token file."""
        with open(self.token_file, "w") as token:
            token.write(self.creds.to_json())
    
    def build_service(self):
        """Build the Google Calendar service object."""
        if self.creds is None:
            raise ValueError("Credentials not loaded. Call load_credentials first.")
        
        self.service = build("calendar", "v3", credentials=self.creds)

    