import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The scope for the Google Sheets API.
# This grants read-only access to all your spreadsheets.
# Use 'https://www.googleapis.com/auth/spreadsheets' for read/write access.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID of the spreadsheet and the range to read from.
# Replace with your actual spreadsheet ID and range.
# For example, 'Sheet1!A1:E10' or 'Form Responses 1!A1:Z'
SPREADSHEET_ID = '1FC8pZ-MzKjZM4rvA6VBDdAkxxzpTGzKIbxQzAIyOk_4'
RANGE_NAME = 'Sheet1!A1:Z'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a specified spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # THIS IS THE CORRECTED OAUTH FLOW FOR TERMINAL-BASED APPS
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print('Please go to this URL to authorize this application:')
            print(auth_url)
            
            # The user must manually copy the URL, authenticate, and then paste the code
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            creds = flow.credentials

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print("Data from Google Sheet:")
        for row in values:
            # Print each row of the data
            print(row)

    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()
