#!/usr/bin/env python3
"""
Test script for the Flask bot management server.
This script demonstrates how to interact with all the server endpoints.
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_bot_registration():
    """Test bot registration."""
    print("🤖 Testing bot registration...")
    
    # Register first bot
    bot1_data = {
        "bot_id": "bot_001",
        "name": "Test Bot 1",
        "version": "1.0.0",
        "status": "active"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=bot1_data)
    print(f"Bot 1 registration - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Register second bot
    bot2_data = {
        "bot_id": "bot_002",
        "name": "Test Bot 2",
        "version": "2.1.0"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=bot2_data)
    print(f"Bot 2 registration - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_list_bots():
    """Test listing all bots."""
    print("📋 Testing bot listing...")
    response = requests.get(f"{BASE_URL}/bots")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_send_commands():
    """Test sending commands to bots."""
    print("📤 Testing command sending...")
    
    # Send command to bot_001
    command_data = {
        "bot_id": "bot_001",
        "command": "start_monitoring",
        "params": {
            "interval": 30,
            "target": "system_metrics"
        }
    }
    
    response = requests.post(f"{BASE_URL}/command", json=command_data)
    print(f"Command to bot_001 - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Send another command
    command_data2 = {
        "bot_id": "bot_001",
        "command": "update_config",
        "params": {
            "log_level": "DEBUG"
        }
    }
    
    response = requests.post(f"{BASE_URL}/command", json=command_data2)
    print(f"Second command to bot_001 - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Try to send command to non-existent bot
    invalid_command = {
        "bot_id": "bot_999",
        "command": "test"
    }
    
    response = requests.post(f"{BASE_URL}/command", json=invalid_command)
    print(f"Command to non-existent bot - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_get_commands():
    """Test getting commands for a bot."""
    print("📥 Testing command retrieval...")
    
    # Get commands for bot_001
    response = requests.get(f"{BASE_URL}/commands/bot_001")
    print(f"Commands for bot_001 - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Try to get commands for non-existent bot
    response = requests.get(f"{BASE_URL}/commands/bot_999")
    print(f"Commands for non-existent bot - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_clear_commands():
    """Test clearing commands for a bot."""
    print("🧹 Testing command clearing...")
    
    response = requests.post(f"{BASE_URL}/commands/bot_001/clear")
    print(f"Clear commands for bot_001 - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_unregister_bot():
    """Test unregistering a bot."""
    print("❌ Testing bot unregistration...")
    
    response = requests.delete(f"{BASE_URL}/bots/bot_002")
    print(f"Unregister bot_002 - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_error_cases():
    """Test various error cases."""
    print("⚠️  Testing error cases...")
    
    # Test registration without required fields
    print("Testing registration without bot_id...")
    response = requests.post(f"{BASE_URL}/register", json={"name": "Invalid Bot"})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test command without required fields
    print("\nTesting command without required fields...")
    response = requests.post(f"{BASE_URL}/command", json={"bot_id": "bot_001"})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test invalid endpoint
    print("\nTesting invalid endpoint...")
    response = requests.get(f"{BASE_URL}/invalid")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("🚀 Starting Flask Bot Management Server Tests\n")
    print("Make sure the server is running: python server_improved.py\n")
    
    try:
        # Run all tests
        test_health_check()
        test_bot_registration()
        test_list_bots()
        test_send_commands()
        test_get_commands()
        test_clear_commands()
        test_get_commands()  # Check that commands were cleared
        test_unregister_bot()
        test_list_bots()  # Check that bot was removed
        test_error_cases()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the server is running: python server_improved.py")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")