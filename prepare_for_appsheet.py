import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def prepare_sheets():
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
        # Get spreadsheet metadata
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        
        # Get sheet IDs
        sheet_ids = {}
        for sheet in spreadsheet['sheets']:
            title = sheet['properties']['title']
            sheet_id = sheet['properties']['sheetId']
            sheet_ids[title] = sheet_id
        
        # Create formatting requests for each sheet
        requests = []
        for title, sheet_id in sheet_ids.items():
            requests.extend([
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': sheet_id,
                            'gridProperties': {
                                'frozenRowCount': 1
                            }
                        },
                        'fields': 'gridProperties.frozenRowCount'
                    }
                },
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                                'textFormat': {'bold': True}
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                }
            ])

        # Execute all formatting requests
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()

        print("Successfully prepared sheets for AppSheet!")
        print("\nNext steps:")
        print("1. Go to https://www.appsheet.com")
        print("2. Sign in with josiah.s.jose@gmail.com")
        print("3. Click 'Create an app'")
        print("4. Choose 'Start with your data'")
        print("5. Select 'Scheduling Assistant Data' spreadsheet")
        print("\nOnce you've done these steps, I'll help configure the AppSheet app with:")
        print("- Calendar view for schedules")
        print("- Client management forms")
        print("- Service catalog")
        print("- Location management")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    prepare_sheets() 