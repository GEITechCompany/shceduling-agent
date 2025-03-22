import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_and_share():
    load_dotenv()
    
    # Load credentials with necessary scopes
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file'
        ]
    )
    
    # Build both services
    sheets = build('sheets', 'v4', credentials=credentials)
    drive = build('drive', 'v3', credentials=credentials)
    
    try:
        # Create new spreadsheet
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
        
        spreadsheet = sheets.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        
        # Share with user
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'josiah.s.jose@gmail.com'
        }
        
        drive.permissions().create(
            fileId=spreadsheet_id,
            body=user_permission,
            sendNotificationEmail=True
        ).execute()
        
        # Update .env file with new spreadsheet ID
        with open('.env', 'r') as file:
            lines = file.readlines()
        
        with open('.env', 'w') as file:
            for line in lines:
                if line.startswith('GOOGLE_SHEETS_SPREADSHEET_ID='):
                    file.write(f'GOOGLE_SHEETS_SPREADSHEET_ID="{spreadsheet_id}"\n')
                else:
                    file.write(line)
        
        print(f"Created and shared new spreadsheet!")
        print(f"Spreadsheet ID: {spreadsheet_id}")
        print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        print(f"Shared with: josiah.s.jose@gmail.com")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    create_and_share() 