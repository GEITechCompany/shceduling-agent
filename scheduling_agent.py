from supabase import create_client
from dotenv import load_dotenv
import os
import datetime
import uuid
from typing import Dict, List, Optional
import re
import json
from openai import OpenAI
import asyncio

# Load environment variables from current directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
print("Looking for .env file at:", env_path)
load_dotenv(env_path)

# Debug: Print current directory and environment variables
print("Current working directory:", os.getcwd())
print("OPENAI_API_KEY exists:", bool(os.getenv('OPENAI_API_KEY')))
print("OPENAI_API_KEY value:", os.getenv('OPENAI_API_KEY')[:10] + "..." if os.getenv('OPENAI_API_KEY') else None)
print("SUPABASE_URL exists:", bool(os.getenv('SUPABASE_URL')))
print("SUPABASE_KEY exists:", bool(os.getenv('SUPABASE_KEY')))

# Check for required environment variables
def check_env_vars():
    required_vars = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_KEY': os.getenv('SUPABASE_KEY')
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return required_vars

# Get environment variables
env_vars = check_env_vars()

# Initialize Supabase client
supabase = create_client(env_vars['SUPABASE_URL'], env_vars['SUPABASE_KEY'])

# Initialize OpenAI client
try:
    client = OpenAI(api_key=env_vars['OPENAI_API_KEY'])
    # Test the connection
    test_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Test"}],
        max_tokens=5
    )
    print("Successfully initialized OpenAI client")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    raise e

class SchedulingAgent:
    def __init__(self):
        try:
            print(f"Connecting to Supabase at {env_vars['SUPABASE_URL']}")
            self.supabase = supabase
            self.client = OpenAI(api_key=env_vars['OPENAI_API_KEY'])  # Initialize OpenAI client here
            print("Successfully connected to Supabase")
        except Exception as e:
            print(f"Error connecting to Supabase: {str(e)}")
            raise e

        self.current_context = {}
        
        # System prompt for ChatGPT
        self.system_prompt = """You are an AI scheduling assistant for a window cleaning and maintenance business. 
        Your role is to help customers schedule appointments, check availability, and manage their bookings.
        
        Available services:
        1. Window Cleaning - $150-300 depending on size
        2. Gutter Cleaning - $100-200
        3. Pressure Washing - $200-400
        4. Solar Panel Cleaning - $250-500
        
        Business hours: Monday-Friday, 9 AM - 5 PM
        Appointment duration: 2-4 hours depending on service
        
        When scheduling:
        1. Collect customer name, service type, preferred date/time
        2. Check availability in the schedule
        3. Confirm booking details
        4. Create appointment in system
        
        Be professional, friendly, and helpful. Always confirm details before making bookings."""
        
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        print("Welcome to the AI Scheduling Assistant! I can help you schedule services and manage appointments. Type 'help' for available commands.")

    async def chat_with_gpt(self, message: str) -> str:
        """Interact with ChatGPT to get more natural responses."""
        try:
            # Add message to conversation history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Get response from ChatGPT
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract and store response
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            print(f"Error in chat_with_gpt: {e}")
            if "invalid_api_key" in str(e):
                return "I apologize, but there seems to be an issue with the API key. Please contact support."
            return "I apologize, but I'm having trouble processing your request. Please try again."

    def extract_intent(self, message: str) -> Dict:
        """Use ChatGPT to extract intent and entities from user message."""
        try:
            prompt = f"""Extract scheduling intent and entities from this message: "{message}"
            Return a JSON object with these fields:
            - intent: search_client, show_schedule, list_services, schedule_service, edit_schedule, delete_schedule, or unknown
            - entities: any relevant names, dates, or services mentioned
            Example: {{"intent": "schedule_service", "entities": {{"client": "John Doe", "service": "window cleaning", "date": "2024-03-25"}}}}
            Response should be valid JSON only."""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a JSON-producing assistant that extracts scheduling intents and entities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error in intent extraction: {str(e)}")
            return {"intent": "unknown", "entities": {}}

    def search_client(self, name: str) -> List[Dict]:
        """Search for a client by name."""
        try:
            print(f"Searching for client with name containing '{name}'")
            response = self.supabase.table('clients').select('*').ilike('name', f'%{name}%').execute()
            print(f"Found {len(response.data)} matching clients")
            return response.data
        except Exception as e:
            print(f"Error searching for client: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response}")
            return []

    def get_client_schedules(self, client_id: str) -> List[Dict]:
        """Get all schedules for a client."""
        try:
            response = self.supabase.table('schedules').select('*').eq('client_id', client_id).execute()
            return response.data
        except Exception as e:
            print(f"Error getting client schedules: {str(e)}")
            return []

    def get_service_details(self, service_id: str) -> Optional[Dict]:
        """Get service details by ID."""
        try:
            response = self.supabase.table('services').select('*').eq('id', service_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting service details: {str(e)}")
            return None

    def get_available_services(self) -> List[Dict]:
        """Get list of available services."""
        try:
            print("Fetching available services from Supabase")
            response = self.supabase.table('services').select('*').execute()
            print(f"Found {len(response.data)} services")
            return response.data
        except Exception as e:
            print(f"Error getting available services: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response}")
            return []

    def validate_date(self, date_str: str) -> bool:
        """Validate if the date is in correct format and in the future."""
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            return date >= datetime.date.today()
        except ValueError:
            return False

    def create_schedule(self, client_id: str, service_id: str, service_date: str, 
                       start_time: str = None, end_time: str = None, notes: str = None) -> Optional[Dict]:
        """Create a new schedule."""
        try:
            if not self.validate_date(service_date):
                raise ValueError("Invalid date or date in the past")

            schedule_data = {
                'id': str(uuid.uuid4()),
                'client_id': client_id,
                'service_id': service_id,
                'service_date': service_date,
                'start_time': start_time,
                'end_time': end_time,
                'notes': notes,
                'status': 'scheduled',
                'location_id': None
            }
            response = self.supabase.table('schedules').insert(schedule_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating schedule: {str(e)}")
            return None

    def select_client(self, selection: str) -> Optional[Dict]:
        """Handle client selection from search results."""
        try:
            if not self.current_context.get('clients'):
                return None
            
            idx = int(selection) - 1
            if 0 <= idx < len(self.current_context['clients']):
                selected_client = self.current_context['clients'][idx]
                self.current_context['selected_client'] = selected_client
                return selected_client
        except ValueError:
            pass
        return None

    def edit_schedule(self, schedule_id: str, updates: Dict) -> Optional[Dict]:
        """Edit an existing schedule."""
        try:
            # Validate date if it's being updated
            if 'service_date' in updates and not self.validate_date(updates['service_date']):
                raise ValueError("Invalid date or date in the past")

            response = self.supabase.table('schedules').update(updates).eq('id', schedule_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error editing schedule: {str(e)}")
            return None

    def delete_schedule(self, schedule_id: str) -> bool:
        """Delete a schedule."""
        try:
            response = self.supabase.table('schedules').delete().eq('id', schedule_id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error deleting schedule: {str(e)}")
            return False

    def get_calendar_data(self, start_date: str, end_date: str) -> List[Dict]:
        """Get all schedules within a date range with client and service details."""
        try:
            response = self.supabase.table('schedules')\
                .select('*, clients(name), services(name)')\
                .gte('service_date', start_date)\
                .lte('service_date', end_date)\
                .execute()
            
            calendar_data = []
            for schedule in response.data:
                calendar_data.append({
                    'id': schedule['id'],
                    'title': f"{schedule['clients']['name']} - {schedule['services']['name']}",
                    'start': schedule['service_date'],
                    'end': schedule['service_date'],
                    'status': schedule['status'],
                    'client_id': schedule['client_id'],
                    'service_id': schedule['service_id'],
                    'notes': schedule['notes']
                })
            return calendar_data
        except Exception as e:
            print(f"Error getting calendar data: {str(e)}")
            return []

    async def process_message(self, message: str) -> str:
        """Process a message from the user and return a response."""
        try:
            # Log the incoming message
            print(f"Processing message: {message[:50]}{'...' if len(message) > 50 else ''}")
            
            # Get response from ChatGPT
            response = await self.chat_with_gpt(message)
            
            # Log the response
            print(f"Generated response: {response[:50]}{'...' if len(response) > 50 else ''}")
            
            return response
        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"I'm sorry, but I encountered an error while processing your request. Please try again later. Error: {str(e)}"

    async def handle_scheduling(self, message: str, gpt_response: str):
        try:
            # Extract scheduling information from the message
            if 'schedule' in message.lower() or 'book' in message.lower():
                # Store in Supabase if needed
                print(f"Processing scheduling request: {message}")
        except Exception as e:
            print(f"Error in handle_scheduling: {e}")

async def main():
    try:
        agent = SchedulingAgent()
        while True:
            try:
                message = input("> ").strip()
                if message.lower() == 'exit':
                    break
                if message:
                    response = await agent.process_message(message)
                    print("\n" + response + "\n")
            except Exception as e:
                print(f"Error: {e}")
                print("Please try again.")
    except Exception as e:
        print(f"Failed to initialize Scheduling Agent: {e}")
        print("Please check your environment variables and try again.")

if __name__ == "__main__":
    asyncio.run(main()) 