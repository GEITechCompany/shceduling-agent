# Scheduling GPT

A simple scheduling assistant application with a modern, compatible interface for scheduling window cleaning and maintenance services.

## Overview

This application includes:

1. A Flask backend API that uses ChatGPT to handle scheduling requests
2. A simple, compatible frontend built with HTML, CSS, and vanilla JavaScript
3. Integration with Supabase for data storage

## Setup

### Prerequisites

- Python 3.6 or later
- An OpenAI API key
- A Supabase account and project

### Environment Variables

Create a `.env` file in the project root with the following:

```
# Supabase credentials
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# OpenAI API key
OPENAI_API_KEY=your_openai_api_key
```

### Installation

1. Install required Python packages:

```bash
pip install flask flask-cors python-dotenv supabase openai
```

2. Verify your setup:

```bash
python test-setup.py
```

This will check if all required files exist and environment variables are set correctly.

## Running the Application

1. Start the server:

```bash
./start-scheduling.sh
```

2. Open your browser and navigate to:

```
http://localhost:5001
```

3. Test the API:

```bash
python test-api.py
```

## Architecture

The application consists of:

- `app.py`: Flask server that handles API requests
- `scheduling_agent.py`: Core logic for interacting with ChatGPT and Supabase
- `simple-scheduling-ui/`: Frontend UI files (HTML, CSS, JS)
- `start-scheduling.sh`: Helper script for starting the application

## Troubleshooting

If you encounter issues:

1. Check if the `.env` file is properly configured
2. Verify that all required Python packages are installed
3. Ensure no other applications are using port 5001
4. Check the Flask server logs for error messages

## License

This project is licensed under the MIT License. 