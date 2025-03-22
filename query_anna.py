from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Supabase client
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# Find Anna Wong's client record
client = supabase.table('clients').select('*').eq('name', 'Anna Wong').execute()
print('\nClient record:')
print(client.data)

if client.data:
    client_id = client.data[0]['id']
    
    # Find associated schedules
    schedules = supabase.table('schedules').select('*').eq('client_id', client_id).execute()
    print('\nSchedules:')
    print(schedules.data)
    
    # Get service IDs from schedules
    service_ids = [s['service_id'] for s in schedules.data if s.get('service_id')]
    if service_ids:
        services = supabase.table('services').select('*').in_('id', service_ids).execute()
        print('\nServices:')
        print(services.data)
    
    # Get location IDs from schedules
    location_ids = [s['location_id'] for s in schedules.data if s.get('location_id')]
    if location_ids:
        locations = supabase.table('locations').select('*').in_('id', location_ids).execute()
        print('\nLocations:')
        print(locations.data) 