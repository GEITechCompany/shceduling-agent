import os

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# Table names
SCHEDULES_TABLE = 'schedules'
CLIENTS_TABLE = 'clients'
SERVICES_TABLE = 'services'
LOCATIONS_TABLE = 'locations'

# Schema definitions
SCHEDULES_SCHEMA = {
    'id': 'uuid',
    'client_id': 'uuid',
    'service_date': 'date',
    'start_time': 'time',
    'end_time': 'time',
    'service_id': 'uuid',
    'location_id': 'uuid',
    'notes': 'text',
    'status': 'text',
    'created_at': 'timestamp with time zone',
    'updated_at': 'timestamp with time zone'
}

CLIENTS_SCHEMA = {
    'id': 'uuid',
    'name': 'text',
    'email': 'text',
    'phone': 'text',
    'address': 'text',
    'city': 'text',
    'postal_code': 'text',
    'notes': 'text',
    'created_at': 'timestamp with time zone',
    'updated_at': 'timestamp with time zone'
}

SERVICES_SCHEMA = {
    'id': 'uuid',
    'name': 'text',
    'description': 'text',
    'duration': 'interval',
    'price': 'numeric',
    'created_at': 'timestamp with time zone',
    'updated_at': 'timestamp with time zone'
}

LOCATIONS_SCHEMA = {
    'id': 'uuid',
    'name': 'text',
    'address': 'text',
    'city': 'text',
    'postal_code': 'text',
    'notes': 'text',
    'created_at': 'timestamp with time zone',
    'updated_at': 'timestamp with time zone'
} 