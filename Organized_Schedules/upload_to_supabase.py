import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import uuid
from datetime import datetime, timedelta
from supabase_config import *

def init_supabase():
    """Initialize Supabase client"""
    load_dotenv()
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_client_data(data):
    """Validate client data before insertion"""
    required_fields = ['name']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure email is valid if provided
    if data.get('email') and '@' not in data['email']:
        raise ValueError("Invalid email format")
    
    return {
        'name': data['name'],
        'email': data.get('email'),
        'phone': data.get('phone'),
        'address': data.get('address'),
        'city': data.get('city'),
        'postal_code': data.get('postal_code'),
        'notes': data.get('notes')
    }

def validate_service_data(data):
    """Validate service data before insertion"""
    required_fields = ['name']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    # Convert duration to proper interval format if provided
    duration = data.get('duration')
    if duration and isinstance(duration, (int, float)):
        data['duration'] = f"{int(duration)} minutes"
    
    return {
        'name': data['name'],
        'description': data.get('description'),
        'duration': data.get('duration'),
        'price': data.get('price')
    }

def validate_location_data(data):
    """Validate location data before insertion"""
    required_fields = ['name']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    return {
        'name': data['name'],
        'address': data.get('address'),
        'city': data.get('city'),
        'postal_code': data.get('postal_code'),
        'notes': data.get('notes')
    }

def validate_schedule_data(data):
    """Validate schedule data before insertion"""
    required_fields = ['client_id', 'service_date']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure service_date is in correct format
    try:
        if isinstance(data['service_date'], str):
            datetime.strptime(data['service_date'], '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid service_date format. Use YYYY-MM-DD")
    
    return {
        'client_id': data['client_id'],
        'service_date': data['service_date'],
        'start_time': data.get('start_time'),
        'end_time': data.get('end_time'),
        'service_id': data.get('service_id'),
        'location_id': data.get('location_id'),
        'notes': data.get('notes'),
        'status': data.get('status', 'scheduled')
    }

def insert_data(supabase, table_name, data, validate_func):
    """Insert data into specified table with validation"""
    try:
        validated_data = validate_func(data)
        response = supabase.table(table_name).insert(validated_data).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error inserting data into {table_name}: {str(e)}")
        raise

def get_or_create_client(supabase, client_data):
    """Get existing client or create new one"""
    try:
        # Check if client exists by email or name
        query = supabase.table(CLIENTS_TABLE)
        if client_data.get('email'):
            response = query.select('*').eq('email', client_data['email']).execute()
        else:
            response = query.select('*').eq('name', client_data['name']).execute()
        
        if response.data:
            return response.data[0]
        
        # Create new client if not found
        return insert_data(supabase, CLIENTS_TABLE, client_data, validate_client_data)
    except Exception as e:
        print(f"Error in get_or_create_client: {str(e)}")
        raise

def get_or_create_service(supabase, service_data):
    """Get existing service or create new one"""
    try:
        # Check if service exists by name
        response = supabase.table(SERVICES_TABLE).select('*').eq('name', service_data['name']).execute()
        
        if response.data:
            return response.data[0]
        
        # Create new service if not found
        return insert_data(supabase, SERVICES_TABLE, service_data, validate_service_data)
    except Exception as e:
        print(f"Error in get_or_create_service: {str(e)}")
        raise

def get_or_create_location(supabase, location_data):
    """Get existing location or create new one"""
    try:
        # Check if location exists by address
        query = supabase.table(LOCATIONS_TABLE)
        if location_data.get('address'):
            response = query.select('*').eq('address', location_data['address']).execute()
            
            if response.data:
                return response.data[0]
        
        # Create new location if not found
        return insert_data(supabase, LOCATIONS_TABLE, location_data, validate_location_data)
    except Exception as e:
        print(f"Error in get_or_create_location: {str(e)}")
        raise

def process_schedule(supabase, schedule_data):
    """Process and insert schedule data"""
    try:
        # Get or create related records
        client = get_or_create_client(supabase, schedule_data['client'])
        service = get_or_create_service(supabase, schedule_data['service'])
        location = get_or_create_location(supabase, schedule_data['location'])
        
        # Prepare schedule data
        schedule = {
            'client_id': client['id'],
            'service_id': service['id'],
            'location_id': location['id'],
            'service_date': schedule_data['service_date'],
            'start_time': schedule_data.get('start_time'),
            'end_time': schedule_data.get('end_time'),
            'notes': schedule_data.get('notes'),
            'status': schedule_data.get('status', 'scheduled')
        }
        
        # Insert schedule
        return insert_data(supabase, SCHEDULES_TABLE, schedule, validate_schedule_data)
    except Exception as e:
        print(f"Error processing schedule: {str(e)}")
        raise

def main():
    """Main function to process and upload data"""
    try:
        # Initialize Supabase client
        supabase = init_supabase()
        
        # Example schedule data (replace with your actual data source)
        schedule_data = {
            'client': {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '123-456-7890'
            },
            'service': {
                'name': 'Window Cleaning',
                'duration': 60,
                'price': 100.00
            },
            'location': {
                'name': 'Home',
                'address': '123 Main St',
                'city': 'Example City',
                'postal_code': '12345'
            },
            'service_date': '2024-03-20',
            'start_time': '09:00',
            'end_time': '10:00',
            'notes': 'Regular cleaning'
        }
        
        # Process schedule
        result = process_schedule(supabase, schedule_data)
        print(f"Successfully created schedule: {result}")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 