import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def configure_sheets():
    load_dotenv()
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    # Build the service
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    
    try:
        # Update column headers to be AppSheet friendly
        updates = [
            {
                'range': 'Clients!A1:G1',
                'values': [['ClientId', 'Name', 'Email', 'Phone', 'Address', 'CreatedAt', 'UpdatedAt']]
            },
            {
                'range': 'Services!A1:G1',
                'values': [['ServiceId', 'Name', 'Description', 'Price', 'DurationMinutes', 'CreatedAt', 'UpdatedAt']]
            },
            {
                'range': 'Schedules!A1:J1',
                'values': [['ScheduleId', 'ClientName', 'ServiceName', 'ServiceDate', 'StartTime', 'EndTime', 'Status', 'Notes', 'CreatedAt', 'UpdatedAt']]
            },
            {
                'range': 'Locations!A1:G1',
                'values': [['LocationId', 'Name', 'Address', 'City', 'PostalCode', 'CreatedAt', 'UpdatedAt']]
            }
        ]

        # Update headers
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                'valueInputOption': 'RAW',
                'data': updates
            }
        ).execute()

        print("Successfully configured sheets for AppSheet!")
        print("\nNow, let's create the AppSheet app:")
        print("1. Open https://www.appsheet.com/create/start")
        print("2. Sign in with josiah.s.jose@gmail.com")
        print("3. Click 'Start with your data'")
        print("4. Select Google Sheets")
        print("5. Choose 'Scheduling Assistant Data'")
        print("6. Wait for me to confirm it's connected, then I'll help configure the app")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    configure_sheets() 