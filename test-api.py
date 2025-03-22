#!/usr/bin/env python3
import requests
import sys
import json

# Configuration
API_URL = "http://localhost:5001/api/chat"
HEALTH_URL = "http://localhost:5001/api/health"
TEST_MESSAGE = "Hello, I'd like to schedule a window cleaning service next week."

def test_health():
    """Test the health check endpoint"""
    print("\n=== Testing Health Endpoint ===")
    try:
        response = requests.get(HEALTH_URL)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Health check passed!")
        else:
            print("❌ Health check failed!")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: The server appears to be down or not accepting connections.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_chat():
    """Test the chat endpoint with a sample message"""
    print("\n=== Testing Chat API ===")
    print(f"Message: '{TEST_MESSAGE}'")
    
    try:
        response = requests.post(
            API_URL,
            json={"message": TEST_MESSAGE},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response preview:")
            if "response" in data:
                preview = data["response"][:100] + "..." if len(data["response"]) > 100 else data["response"]
                print(f"{preview}")
                print("✅ API test passed!")
            else:
                print(f"Unexpected response format: {json.dumps(data, indent=2)}")
                print("❌ API test failed: Unexpected response format")
        else:
            try:
                print(f"Error: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Error: {response.text}")
            print("❌ API test failed!")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: The server appears to be down or not accepting connections.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def check_frontend():
    """Check if the frontend is accessible"""
    print("\n=== Testing Frontend ===")
    try:
        response = requests.get("http://localhost:5001/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
        else:
            print("❌ Frontend check failed!")
            print(f"Response: {response.text[:100]}...")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: The server appears to be down or not accepting connections.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=== Scheduling GPT API Test ===")
    print("Testing API endpoints...\n")
    
    check_frontend()
    test_health()
    test_chat()
    
    print("\nTests completed!") 