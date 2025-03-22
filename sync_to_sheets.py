import os
from dotenv import load_dotenv
from supabase import create_client
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import datetime

class DataSyncer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Supabase client
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        # Initialize Google Sheets client
        self.sheets_service = self._init_sheets_service()
        self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')

    def _init_sheets_service(self):
        """Initialize Google Sheets service with credentials."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(f"Error initializing Google Sheets service: {str(e)}")
            raise

    def _format_date(self, date_str):
        """Format date string for Google Sheets."""
        if not date_str:
            return ''
        try:
            date = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return date_str

    def sync_clients(self):
        """Sync clients data from Supabase to Google Sheets."""
        try:
            # Fetch clients from Supabase
            response = self.supabase.table('clients').select('*').execute()
            clients = response.data

            # Prepare data for Google Sheets
            values = [['ID', 'Name', 'Email', 'Phone', 'Address', 'Created At', 'Updated At']]
            for client in clients:
                values.append([
                    client['id'],
                    client['name'],
                    client.get('email', ''),
                    client.get('phone', ''),
                    client.get('address', ''),
                    self._format_date(client.get('created_at')),
                    self._format_date(client.get('updated_at'))
                ])

            # Update Google Sheet
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Clients!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            print(f"Successfully synced {len(clients)} clients")

        except Exception as e:
            print(f"Error syncing clients: {str(e)}")

    def sync_services(self):
        """Sync services data from Supabase to Google Sheets."""
        try:
            # Fetch services from Supabase
            response = self.supabase.table('services').select('*').execute()
            services = response.data

            # Prepare data for Google Sheets
            values = [['ID', 'Name', 'Description', 'Price', 'Duration (Minutes)', 'Created At', 'Updated At']]
            for service in services:
                values.append([
                    service['id'],
                    service['name'],
                    service.get('description', ''),
                    service.get('price', 0),
                    service.get('duration_minutes', 0),
                    self._format_date(service.get('created_at')),
                    self._format_date(service.get('updated_at'))
                ])

            # Update Google Sheet
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Services!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            print(f"Successfully synced {len(services)} services")

        except Exception as e:
            print(f"Error syncing services: {str(e)}")

    def sync_schedules(self):
        """Sync schedules data from Supabase to Google Sheets."""
        try:
            # Fetch schedules with client and service names
            response = self.supabase.table('schedules')\
                .select('*, clients(name), services(name)')\
                .execute()
            schedules = response.data

            # Prepare data for Google Sheets
            values = [['ID', 'Client Name', 'Service Name', 'Service Date', 'Start Time', 
                      'End Time', 'Status', 'Notes', 'Created At', 'Updated At']]
            for schedule in schedules:
                values.append([
                    schedule['id'],
                    schedule['clients']['name'],
                    schedule['services']['name'],
                    schedule['service_date'],
                    schedule.get('start_time', ''),
                    schedule.get('end_time', ''),
                    schedule.get('status', 'scheduled'),
                    schedule.get('notes', ''),
                    self._format_date(schedule.get('created_at')),
                    self._format_date(schedule.get('updated_at'))
                ])

            # Update Google Sheet
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Schedules!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            print(f"Successfully synced {len(schedules)} schedules")

        except Exception as e:
            print(f"Error syncing schedules: {str(e)}")

    def sync_locations(self):
        """Sync locations data from Supabase to Google Sheets."""
        try:
            # Fetch locations from Supabase
            response = self.supabase.table('locations').select('*').execute()
            locations = response.data

            # Prepare data for Google Sheets
            values = [['ID', 'Name', 'Address', 'City', 'Postal Code', 'Created At', 'Updated At']]
            for location in locations:
                values.append([
                    location['id'],
                    location['name'],
                    location.get('address', ''),
                    location.get('city', ''),
                    location.get('postal_code', ''),
                    self._format_date(location.get('created_at')),
                    self._format_date(location.get('updated_at'))
                ])

            # Update Google Sheet
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Locations!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            print(f"Successfully synced {len(locations)} locations")

        except Exception as e:
            print(f"Error syncing locations: {str(e)}")

    def sync_all(self):
        """Sync all data from Supabase to Google Sheets."""
        print("Starting data sync...")
        self.sync_clients()
        self.sync_services()
        self.sync_locations()
        self.sync_schedules()
        print("Data sync completed!")

def main():
    syncer = DataSyncer()
    syncer.sync_all()

if __name__ == "__main__":
    main() 