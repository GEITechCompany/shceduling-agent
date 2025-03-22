import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_sheets_connection():
    load_dotenv()
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    # Build the service
    service = build('sheets', 'v4', credentials=credentials)
    
    try:
        # Create a new sheet to test the connection
        spreadsheet = {
            'properties': {
                'title': 'Scheduling Assistant Data'
            },
            'sheets': [
                {'properties': {'title': 'Clients'}},
                {'properties': {'title': 'Services'}},
                {'properties': {'title': 'Schedules'}},
                {'properties': {'title': 'Locations'}}
            ]
        }
        
        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        print(f"Created new spreadsheet!")
        print(f"Spreadsheet ID: {spreadsheet_id}")
        print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        print("\nSheets created:")
        for sheet in spreadsheet['sheets']:
            print(f"- {sheet['properties']['title']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_sheets_connection() 