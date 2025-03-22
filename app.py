from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from scheduling_agent import SchedulingAgent
import asyncio
import os
import traceback
from functools import wraps

# Set static folder to our simple UI
app = Flask(__name__, static_folder='simple-scheduling-ui')
CORS(app)  # Enable CORS for all routes
agent = None
loop = None

# Print startup info
print("\n=== Scheduling GPT API Server ===")
print(f"Current directory: {os.getcwd()}")
print(f"Static folder: {app.static_folder}")
print(f"Static files exist: {os.path.exists(app.static_folder)}")
print(f"Files in static folder: {os.listdir(app.static_folder) if os.path.exists(app.static_folder) else 'N/A'}")

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(f(*args, **kwargs))
    return wrapped

@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        traceback.print_exc()
        return f"Error serving the application: {str(e)}", 500

@app.route('/<path:path>')
def static_files(path):
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        print(f"Error serving static file {path}: {e}")
        return f"Error serving {path}: {str(e)}", 404

@app.route('/api/chat', methods=['POST'])
@async_route
async def chat():
    global agent
    if agent is None:
        try:
            print("Initializing scheduling agent...")
            agent = SchedulingAgent()
            print("Scheduling agent initialized successfully!")
        except Exception as e:
            error_msg = f"Error initializing agent: {e}"
            print(error_msg)
            traceback.print_exc()
            return jsonify({'error': error_msg}), 500
    
    data = request.json
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400
        
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
        
    print(f"Received message: {message[:50]}{'...' if len(message) > 50 else ''}")
    
    try:
        print("Processing message...")
        response = await agent.process_message(message)
        print(f"Response: {response[:50]}{'...' if len(response) > 50 else ''}")
        return jsonify({'response': response})
    except Exception as e:
        error_msg = f"Error processing message: {e}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'agent_initialized': agent is not None
    })

def run_app():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        host = "0.0.0.0"  # Listen on all interfaces
        port = 5001
        print(f"\nStarting Flask server on http://localhost:{port}")
        print("API endpoints:")
        print(f"  - http://localhost:{port}/api/chat (POST)")
        print(f"  - http://localhost:{port}/api/health (GET)")
        print("\nFrontend:")
        print(f"  - http://localhost:{port}/")
        print("\nPress Ctrl+C to stop the server")
        app.run(host=host, port=port, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        traceback.print_exc()
    finally:
        if loop:
            loop.close()

if __name__ == '__main__':
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_app() 