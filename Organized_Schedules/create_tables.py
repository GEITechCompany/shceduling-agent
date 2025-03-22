import os
from supabase import create_client
from dotenv import load_dotenv
from supabase_config import *

def init_supabase():
    """Initialize Supabase client"""
    load_dotenv()
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables(supabase):
    """Create tables in Supabase"""
    try:
        print("\nCreating clients table...")
        # Create clients table
        response = supabase.table(CLIENTS_TABLE).insert({
            'name': 'Test Client',
            'email': 'test@example.com',
            'phone': '123-456-7890',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '12345',
            'notes': 'Test client for table creation'
        }).execute()
        print("Clients table created successfully!")
        
        print("\nCreating services table...")
        # Create services table
        response = supabase.table(SERVICES_TABLE).insert({
            'name': 'Test Service',
            'description': 'Test service description',
            'duration': '1 hour',
            'price': 100.00
        }).execute()
        print("Services table created successfully!")
        
        print("\nCreating locations table...")
        # Create locations table
        response = supabase.table(LOCATIONS_TABLE).insert({
            'name': 'Test Location',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '12345',
            'notes': 'Test location for table creation'
        }).execute()
        print("Locations table created successfully!")
        
        print("\nCreating schedules table...")
        # Create schedules table
        response = supabase.table(SCHEDULES_TABLE).insert({
            'client_id': response.data[0]['id'],  # Use the ID from the test client
            'service_date': '2024-03-20',
            'start_time': '09:00',
            'end_time': '10:00',
            'service_id': response.data[0]['id'],  # Use the ID from the test service
            'location_id': response.data[0]['id'],  # Use the ID from the test location
            'notes': 'Test schedule for table creation',
            'status': 'scheduled'
        }).execute()
        print("Schedules table created successfully!")
        
        print("\nAll tables created successfully!")
        
        # Clean up test data
        print("\nCleaning up test data...")
        supabase.table(SCHEDULES_TABLE).delete().eq('notes', 'Test schedule for table creation').execute()
        supabase.table(LOCATIONS_TABLE).delete().eq('notes', 'Test location for table creation').execute()
        supabase.table(SERVICES_TABLE).delete().eq('description', 'Test service description').execute()
        supabase.table(CLIENTS_TABLE).delete().eq('notes', 'Test client for table creation').execute()
        print("Test data cleaned up successfully!")
        
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        raise

def main():
    """Main function to create database tables"""
    try:
        # Initialize Supabase client
        supabase = init_supabase()
        
        # Create tables
        create_tables(supabase)
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 