import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def check_sheets():
    load_dotenv()
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    # Build the service
    service = build('sheets', 'v4', credentials=credentials)
    
    # Get spreadsheet ID from env
    spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    
    try:
        # Check each sheet
        sheets = ['Clients', 'Services', 'Schedules', 'Locations']
        for sheet in sheets:
            print(f"\nChecking {sheet} sheet:")
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet}!A1:Z5"  # Get first 5 rows including headers
            ).execute()
            
            if 'values' in result:
                # Print headers
                print("\nHeaders:")
                print(", ".join(result['values'][0]))
                
                # Print first few rows
                print("\nFirst few rows:")
                for row in result['values'][1:4]:  # Print up to 3 data rows
                    print(row)
                
                # Get total row count
                row_count = len(service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range=f"{sheet}!A:A"
                ).execute().get('values', []))
                print(f"\nTotal rows: {row_count}")
            else:
                print("No data found in sheet")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_sheets() 