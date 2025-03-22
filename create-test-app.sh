#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Create a test React app in a new directory
echo "Creating test React app..."
mkdir -p test-react-app
cd test-react-app

# Create minimal package.json
cat > package.json << 'EOF'
{
  "name": "test-react-app",
  "version": "1.0.0",
  "scripts": {
    "start": "echo 'Test React app script executed successfully!'"
  }
}
EOF

echo "Test app created at $(pwd)"
echo "Running test app:"
npm start

echo ""
echo "If the test app works but your main app doesn't, there may be an issue with your main React app configuration."
echo "Try running: cd $(pwd) && npm start" 