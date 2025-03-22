import os
import pandas as pd
from datetime import datetime
from upload_to_supabase import process_schedule

def clean_amount(amount_str):
    """Clean amount string and convert to float"""
    try:
        if not amount_str or pd.isna(amount_str):
            return 0.0
        # Remove currency symbols, commas, and spaces
        cleaned = str(amount_str).replace('$', '').replace(',', '').replace(' ', '')
        # Convert to float
        return float(cleaned or 0)
    except ValueError:
        print(f"Warning: Invalid amount format: {amount_str}")
        return 0.0

def parse_quickbooks_csv(file_path):
    """Parse QuickBooks CSV file with services as columns"""
    try:
        print(f"\nProcessing file: {file_path}")
        
        # Read CSV file, skip the first few rows that contain headers
        df = pd.read_csv(file_path, skiprows=4)
        
        # Get the year from the filename
        year = None
        if '2022' in file_path:
            year = '2022'
        elif '2023' in file_path:
            year = '2023'
        elif '2024' in file_path:
            year = '2024'
        
        if not year:
            print(f"Warning: Could not determine year from filename: {file_path}")
            return []
        
        schedules = []
        # Process each row (client)
        for _, row in df.iterrows():
            client_name = row.iloc[0]  # First column is client name
            if not client_name or pd.isna(client_name):
                continue
                
            # Process each service column
            for service_name in df.columns[1:-1]:  # Skip first (client) and last (total) columns
                amount = clean_amount(row[service_name])
                if amount > 0:  # Only process non-zero amounts
                    schedule_data = {
                        'client': {
                            'name': client_name.strip(),
                            'email': '',  # Not available in this format
                            'phone': '',  # Not available in this format
                            'address': '',  # Not available in this format
                            'city': '',  # Not available in this format
                            'postal_code': ''  # Not available in this format
                        },
                        'service': {
                            'name': service_name.strip(),
                            'description': '',  # Not available in this format
                            'duration': 60,  # Default duration
                            'price': amount
                        },
                        'location': {
                            'name': 'Primary Location',
                            'address': '',  # Not available in this format
                            'city': '',  # Not available in this format
                            'postal_code': ''  # Not available in this format
                        },
                        'service_date': f"{year}-01-01",  # Default to January 1st of the year
                        'notes': f"Imported from {os.path.basename(file_path)}",
                        'status': 'estimated'
                    }
                    schedules.append(schedule_data)
        
        return schedules
    
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return []

def main():
    """Main function to process all estimate files"""
    try:
        # Process all CSV files in the History CSV directory
        csv_dir = "History CSV"
        all_schedules = []
        
        for root, _, files in os.walk(csv_dir):
            for file in files:
                if file.lower().startswith('quickbooks') and file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    schedules = parse_quickbooks_csv(file_path)
                    all_schedules.extend(schedules)
        
        print(f"\nFound {len(all_schedules)} valid schedules to process")
        
        # Initialize Supabase and process schedules
        from upload_to_supabase import init_supabase
        supabase = init_supabase()
        
        # Process each schedule
        for i, schedule_data in enumerate(all_schedules, 1):
            try:
                print(f"\nProcessing schedule {i}/{len(all_schedules)}")
                result = process_schedule(supabase, schedule_data)
                print(f"Successfully created schedule: {result['id']}")
            except Exception as e:
                print(f"Error processing schedule: {str(e)}")
                continue
        
        print("\nFinished processing all schedules")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 