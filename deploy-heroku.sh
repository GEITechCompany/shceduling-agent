#!/bin/bash

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI is not installed. Installing..."
    brew tap heroku/brew && brew install heroku
fi

# Login to Heroku
echo "Logging into Heroku..."
heroku login

# Create a new Heroku app (if not already created)
if [ ! -f ".heroku/app.json" ]; then
    echo "Creating new Heroku app..."
    heroku create scheduling-gpt-assistant
fi

# Set up environment variables
echo "Setting up environment variables..."
heroku config:set OPENAI_API_KEY="$OPENAI_API_KEY"
heroku config:set SUPABASE_URL="$SUPABASE_URL"
heroku config:set SUPABASE_KEY="$SUPABASE_KEY"

# Create a temporary directory for deployment
echo "Preparing files for deployment..."
mkdir -p deploy_temp
cp -r app.py scheduling_agent.py requirements.txt Procfile simple-scheduling-ui deploy_temp/

# Initialize git in the temporary directory
cd deploy_temp
git init
git add .
git commit -m "Deploy to Heroku"

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku main --force

# Clean up
cd ..
rm -rf deploy_temp

# Get the app URL
APP_URL=$(heroku info -s | grep "Web URL" | cut -d= -f2)
echo "Your app is deployed at: $APP_URL"
echo "API endpoint: $APP_URL/api/chat" 