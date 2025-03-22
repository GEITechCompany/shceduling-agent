import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def update_permissions():
    load_dotenv()
    
    print("To share the spreadsheet:")
    print("1. Open this URL in your browser:")
    print(f"https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')}")
    print("\n2. Click the 'Share' button in the top right")
    print("3. Click 'Change to anyone with the link'")
    print("4. Set the permission to 'Viewer'")
    print("5. Click 'Done'")
    print("\nAfter doing this, please share the link with me and I'll verify the access.")

if __name__ == "__main__":
    update_permissions() 