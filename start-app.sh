#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Change to the React app directory 
echo "Script location: $(dirname "$0")"
cd "$(dirname "$0")/scheduling-gpt-frontend" || {
    echo "Error: Failed to change to scheduling-gpt-frontend directory"
    exit 1
}

# Print current directory for confirmation
echo "Starting React app from directory: $(pwd)"
echo "Contents of current directory:"
ls -la

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found in $(pwd)"
    exit 1
fi

# Check npm scripts
echo "Available npm scripts:"
npm run --silent || true

# Start the React app
echo "Starting npm..."
npm start 