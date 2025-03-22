#!/bin/bash

# Scheduling Assistant Backend Deployment Script
# This script helps deploy your Flask backend to a VPS

# Colors for prettier output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}    Scheduling Assistant Backend Deployment Tool    ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo 

# Check if necessary commands exist
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is required but not found${NC}"
        exit 1
    fi
}

check_command python3
check_command pip3
check_command scp
check_command ssh

# Function to ask for input with a default value
ask_with_default() {
    local prompt=$1
    local default=$2
    local input
    
    echo -ne "${YELLOW}$prompt${NC} [$default]: "
    read input
    echo "${input:-$default}"
}

# Ask for server details
echo -e "${GREEN}Server Information${NC}"
echo "Please provide details about your VPS:"
SERVER_USER=$(ask_with_default "Username" "root")
SERVER_IP=$(ask_with_default "Server IP Address" "your-server-ip")
SERVER_PORT=$(ask_with_default "SSH Port" "22")
SERVER_PATH=$(ask_with_default "Deployment Path" "/var/www/scheduling-assistant")

# Confirm
echo
echo -e "${GREEN}Deployment Configuration:${NC}"
echo -e "  Server: ${SERVER_USER}@${SERVER_IP}:${SERVER_PORT}"
echo -e "  Path: ${SERVER_PATH}"
echo

read -p "Continue with deployment? (y/n): " CONFIRM
if [[ $CONFIRM != "y" && $CONFIRM != "Y" ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Create deployment package
echo -e "\n${GREEN}Creating deployment package...${NC}"
mkdir -p deploy
cp -r app.py scheduling_agent.py requirements.txt .env start-scheduling.sh test-api.py deploy/
chmod +x deploy/start-scheduling.sh

echo -e "\n${GREEN}Creating server setup script...${NC}"
cat > deploy/setup-server.sh << 'EOF'
#!/bin/bash

# Server setup script for Scheduling Assistant

# Install required packages
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-venv nginx supervisor

# Create a Python virtual environment
echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create Supervisor configuration
echo "Configuring Supervisor..."
cat > /etc/supervisor/conf.d/scheduling-assistant.conf << 'EOL'
[program:scheduling-assistant]
directory=/var/www/scheduling-assistant
command=/var/www/scheduling-assistant/venv/bin/python app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/scheduling-assistant.err.log
stdout_logfile=/var/log/scheduling-assistant.out.log
EOL

# Create Nginx configuration for reverse proxy
echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/scheduling-assistant << 'EOL'
server {
    listen 80;
    server_name api.yourdomain.com;  # Change this to your domain or IP

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOL

# Enable the Nginx site
ln -sf /etc/nginx/sites-available/scheduling-assistant /etc/nginx/sites-enabled/

# Restart services
echo "Restarting services..."
supervisorctl reload
nginx -t && systemctl restart nginx

echo "Setup complete!"
echo "Please edit /etc/nginx/sites-available/scheduling-assistant to set your domain name"
echo "Then restart Nginx with: systemctl restart nginx"
EOF

chmod +x deploy/setup-server.sh

# Deploy to server
echo -e "\n${GREEN}Deploying to server...${NC}"
ssh -p ${SERVER_PORT} ${SERVER_USER}@${SERVER_IP} "mkdir -p ${SERVER_PATH}"
scp -P ${SERVER_PORT} -r deploy/* ${SERVER_USER}@${SERVER_IP}:${SERVER_PATH}/

echo -e "\n${GREEN}Deployment complete!${NC}"
echo "To finish setup on your server, run the following commands:"
echo -e "${YELLOW}  ssh -p ${SERVER_PORT} ${SERVER_USER}@${SERVER_IP}${NC}"
echo -e "${YELLOW}  cd ${SERVER_PATH}${NC}"
echo -e "${YELLOW}  sudo ./setup-server.sh${NC}"

echo
echo -e "${GREEN}After setup is complete:${NC}"
echo -e "1. Update your .env file on the server with your credentials"
echo -e "2. Edit the Nginx config to use your domain name"
echo -e "3. Adjust the CORS settings in app.py to allow your frontend domain"
echo
echo -e "${GREEN}Your API will be available at: http://your-server-ip/api/chat${NC}"
echo

# Clean up
rm -rf deploy 