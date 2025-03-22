#!/bin/bash

# Print header
echo "======================================================="
echo "Starting Scheduling GPT Application"
echo "======================================================="
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Check if all required packages are installed
REQUIRED_PACKAGES=("flask" "flask-cors" "python-dotenv" "supabase" "openai")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    python3 -c "import $package" 2>/dev/null || MISSING_PACKAGES+=("$package")
done

# Install missing packages if needed
if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "Installing required packages: ${MISSING_PACKAGES[*]}"
    pip3 install ${MISSING_PACKAGES[*]}
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please make sure you have set up your environment variables."
    echo "Creating sample .env file..."
    cat > .env << EOF
# Supabase credentials
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# OpenAI API key
OPENAI_API_KEY=your_openai_api_key
EOF
    echo "Please edit the .env file with your actual credentials."
fi

# Start the Flask server
echo "Starting Flask server..."
python3 app.py 