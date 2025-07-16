#!/usr/bin/env python3
"""
Example bot client that demonstrates how to interact with the bot management server.
This bot will register itself, poll for commands, and execute them.
"""

import requests
import json
import time
import threading
import signal
import sys
from datetime import datetime

class BotClient:
    def __init__(self, bot_id, bot_name, server_url="http://localhost:5000"):
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.server_url = server_url
        self.running = False
        self.poll_interval = 5  # Poll every 5 seconds
        
    def register(self):
        """Register this bot with the server."""
        registration_data = {
            "bot_id": self.bot_id,
            "name": self.bot_name,
            "version": "1.0.0",
            "status": "active",
            "capabilities": ["monitoring", "file_operations", "system_info"]
        }
        
        try:
            response = requests.post(f"{self.server_url}/register", json=registration_data)
            if response.status_code == 200:
                print(f"✅ Bot {self.bot_id} registered successfully!")
                return True
            else:
                print(f"❌ Failed to register bot: {response.json()}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error during registration: {e}")
            return False
    
    def poll_commands(self):
        """Poll for commands from the server."""
        try:
            response = requests.get(f"{self.server_url}/commands/{self.bot_id}")
            if response.status_code == 200:
                data = response.json()
                commands = data.get('commands', [])
                if commands:
                    print(f"📥 Received {len(commands)} command(s)")
                    return commands
                return []
            elif response.status_code == 404:
                print(f"⚠️ Bot {self.bot_id} is not registered!")
                return None
            else:
                print(f"❌ Error polling commands: {response.json()}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error while polling: {e}")
            return []
    
    def execute_command(self, command_data):
        """Execute a command (simulate command execution)."""
        command = command_data.get('command')
        params = command_data.get('params', {})
        timestamp = command_data.get('timestamp')
        
        print(f"🔧 Executing command: {command}")
        print(f"   Parameters: {params}")
        print(f"   Received at: {timestamp}")
        
        # Simulate command execution based on command type
        if command == "status_check":
            print("   Status: Bot is running normally")
            time.sleep(1)  # Simulate work
            
        elif command == "start_monitoring":
            interval = params.get('interval', 60)
            target = params.get('target', 'default')
            print(f"   Starting monitoring of {target} with {interval}s interval")
            time.sleep(2)  # Simulate work
            
        elif command == "update_config":
            log_level = params.get('log_level', 'INFO')
            print(f"   Updated log level to {log_level}")
            time.sleep(0.5)  # Simulate work
            
        elif command == "get_system_info":
            print("   Gathering system information...")
            time.sleep(1.5)  # Simulate work
            print("   System info: CPU: 45%, Memory: 62%, Disk: 78%")
            
        elif command == "restart":
            print("   Restarting bot (simulated)...")
            time.sleep(3)  # Simulate restart time
            
        else:
            print(f"   ⚠️ Unknown command: {command}")
        
        print(f"✅ Command '{command}' completed")
    
    def clear_commands(self):
        """Clear processed commands from the server."""
        try:
            response = requests.post(f"{self.server_url}/commands/{self.bot_id}/clear")
            if response.status_code == 200:
                data = response.json()
                cleared_count = data.get('cleared_count', 0)
                if cleared_count > 0:
                    print(f"🧹 Cleared {cleared_count} processed command(s)")
                return True
            else:
                print(f"❌ Error clearing commands: {response.json()}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error while clearing commands: {e}")
            return False
    
    def run(self):
        """Main bot loop."""
        print(f"🤖 Starting bot {self.bot_id} ({self.bot_name})")
        
        # Register with server
        if not self.register():
            print("❌ Failed to register. Exiting.")
            return
        
        self.running = True
        print(f"🔄 Starting command polling loop (every {self.poll_interval}s)")
        
        while self.running:
            try:
                # Poll for commands
                commands = self.poll_commands()
                
                if commands is None:  # Bot not registered
                    print("🔄 Attempting to re-register...")
                    if not self.register():
                        print("❌ Re-registration failed. Waiting before retry...")
                        time.sleep(10)
                        continue
                
                if commands:
                    # Execute all commands
                    for command_data in commands:
                        if not self.running:
                            break
                        self.execute_command(command_data)
                    
                    # Clear processed commands
                    self.clear_commands()
                
                # Wait before next poll
                for _ in range(self.poll_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Unexpected error in main loop: {e}")
                time.sleep(5)
        
        self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown the bot."""
        print(f"\n🛑 Shutting down bot {self.bot_id}...")
        self.running = False
        
        # Optionally unregister from server
        try:
            response = requests.delete(f"{self.server_url}/bots/{self.bot_id}")
            if response.status_code == 200:
                print("✅ Bot unregistered successfully")
            else:
                print("⚠️ Failed to unregister bot")
        except:
            print("⚠️ Could not unregister bot (server may be down)")
        
        print("👋 Bot shutdown complete")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    print("\n🛑 Received shutdown signal...")
    if 'bot' in globals():
        bot.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run bot
    bot_id = "example_bot_001"
    bot_name = "Example Bot Client"
    
    print("🚀 Example Bot Client")
    print(f"Bot ID: {bot_id}")
    print(f"Bot Name: {bot_name}")
    print("Make sure the server is running: python server_improved.py")
    print("Press Ctrl+C to stop the bot\n")
    
    bot = BotClient(bot_id, bot_name)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        if bot.running:
            bot.shutdown()