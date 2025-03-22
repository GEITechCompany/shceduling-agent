# Scheduling Assistant Frontend

A modern, responsive frontend for the Scheduling Assistant application, optimized for deployment on Hostinger.

## Overview

This frontend is built with plain HTML, CSS, and JavaScript, making it compatible with any standard web hosting service like Hostinger. It connects to your existing Flask backend API.

## File Structure

- `index.html` - Main HTML file
- `styles.css` - CSS styles
- `config.js` - Configuration settings
- `app.js` - Application logic
- `favicon.ico` - Site favicon

## Deployment to Hostinger

Follow these steps to deploy this frontend to Hostinger:

1. **Log in to your Hostinger account**

2. **Upload Files**
   - Go to File Manager in your Hostinger control panel
   - Navigate to your domain's public_html directory
   - Upload all files from this folder to the public_html directory
   - Alternatively, you can use FTP to upload the files

3. **Configure API Connection**
   - Once deployed, visit your website
   - Click the settings icon (gear) in the chat interface
   - Enter your API backend URL (e.g., `https://your-api-domain.com/api/chat`)
   - If your API requires authentication, enter your API key
   - Click "Save Settings"

## Backend API Requirements

Your existing Flask backend already meets these requirements, but for reference, the frontend expects:

1. POST requests to the endpoint `/api/chat` with JSON containing a `message` field:
   ```json
   { "message": "I want to schedule a window cleaning service" }
   ```

2. Response with JSON containing a `response` field:
   ```json
   { "response": "I'd be happy to help schedule that. When would you like the service?" }
   ```

3. A health check endpoint at `/api/health` (optional but recommended)

## Running Your Existing Flask Backend

Your Flask application (`app.py`) is already set up correctly with:
- CORS configuration to allow cross-domain requests
- The correct API endpoints for chat and health checks
- Proper error handling

To run your backend:

1. Ensure your environment variables are set in the `.env` file:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENAI_API_KEY=your_openai_api_key
   ```

2. Run the start script:
   ```bash
   ./start-scheduling.sh
   ```

3. Your backend will be available at http://localhost:5001

## Deployment Options for the Backend

To make your backend accessible from your Hostinger frontend:

1. **VPS/Dedicated Server**
   - Deploy your Flask app on a VPS from DigitalOcean, Linode, or AWS EC2
   - Use a reverse proxy like Nginx or Apache
   - Consider setting up a domain or subdomain for your API

2. **PaaS Options**
   - Heroku: Easy deployment with `Procfile` and `requirements.txt`
   - Render: Similar to Heroku with simple Git-based deployments
   - PythonAnywhere: Good for Python-specific applications

3. **Serverless Options**
   - AWS Lambda with API Gateway
   - Google Cloud Functions
   - Azure Functions

Remember to update your CORS settings in production to only allow your specific frontend domain:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://your-frontend-domain.com"}})
```

## Troubleshooting

If the assistant doesn't work after deployment:

1. Check the browser console for errors (F12 in most browsers)
2. Verify your API URL in the settings
3. Ensure your backend is running and accessible
4. Check if CORS is properly configured on your backend
5. Test your backend with the included `test-api.py` script

# Scheduling Assistant Integration Guide

## Overview
This guide explains how to integrate the Scheduling Assistant with your Hostinger website.

## Integration Steps

### 1. Upload Files
1. Log in to your Hostinger control panel
2. Navigate to the File Manager
3. Upload the following files to your website's root directory:
   - `index.html`
   - `app.js`
   - `config.js`
   - `styles.css`
   - `favicon.ico`

### 2. Add to Your Website
Add the following code to your website's HTML where you want the scheduling assistant to appear:

```html
<!-- Add this in the <head> section -->
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

<!-- Add this where you want the chat widget to appear -->
<div id="scheduling-assistant"></div>

<!-- Add these before the closing </body> tag -->
<script src="config.js"></script>
<script src="app.js"></script>
```

### 3. Customize Appearance
You can customize the appearance by modifying the `styles.css` file. The main elements you can style are:
- `#scheduling-assistant` - The main container
- `.chat-widget` - The chat interface
- `.service-list` - The list of available services

### 4. Test the Integration
1. Visit your website
2. Click the scheduling assistant widget
3. Try scheduling a service to ensure everything works correctly

## Troubleshooting

### Common Issues
1. **Widget Not Appearing**
   - Check if all files are uploaded correctly
   - Verify file paths in your HTML
   - Check browser console for errors

2. **API Connection Issues**
   - Verify the API URL in `config.js`
   - Check if your Heroku app is running
   - Ensure CORS is properly configured

3. **Styling Issues**
   - Check if `styles.css` is loading correctly
   - Verify Font Awesome is loading
   - Check for CSS conflicts with your main site

## Support
If you encounter any issues:
1. Check the browser console for error messages
2. Verify all files are uploaded correctly
3. Ensure your Heroku backend is running
4. Contact support if issues persist

## Security Notes
- The API key is stored in your Heroku environment variables
- All API calls are made over HTTPS
- No sensitive data is stored in the frontend 