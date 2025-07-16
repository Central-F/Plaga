from flask import Flask, request, jsonify
import logging
import threading
import time
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bots: Dict[str, Dict[str, Any]] = {}
bot_commands: Dict[str, list] = {}  # Store commands for each bot
bot_lock = threading.Lock()

def validate_json_data(data: dict, required_fields: list) -> tuple[bool, str]:
    """Validate that required fields are present in the JSON data."""
    if not data:
        return False, "No JSON data provided"
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not data[field] or not str(data[field]).strip():
            return False, f"Field '{field}' cannot be empty"
    
    return True, ""

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "registered_bots": len(bots)
    })

@app.route('/register', methods=['POST'])
def register():
    """Register a new bot or update existing bot information."""
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error_msg = validate_json_data(data, ['bot_id'])
        if not is_valid:
            logger.warning(f"Registration failed: {error_msg}")
            return jsonify({"status": "error", "message": error_msg}), 400
        
        bot_id = data['bot_id']
        
        with bot_lock:
            # Add registration timestamp
            data['registered_at'] = datetime.now().isoformat()
            data['last_seen'] = datetime.now().isoformat()
            
            # Initialize command queue for new bot
            if bot_id not in bot_commands:
                bot_commands[bot_id] = []
            
            bots[bot_id] = data
        
        logger.info(f"Bot {bot_id} registered successfully")
        return jsonify({
            "status": "success",
            "message": f"Bot {bot_id} registered successfully",
            "bot_id": bot_id
        })
        
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/command', methods=['POST'])
def send_command():
    """Send a command to a specific bot."""
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error_msg = validate_json_data(data, ['bot_id', 'command'])
        if not is_valid:
            logger.warning(f"Command failed: {error_msg}")
            return jsonify({"status": "error", "message": error_msg}), 400
        
        bot_id = data['bot_id']
        command = data['command']
        
        with bot_lock:
            if bot_id not in bots:
                logger.warning(f"Command failed: Bot {bot_id} not found")
                return jsonify({
                    "status": "error", 
                    "message": f"Bot {bot_id} is not registered"
                }), 404
            
            # Add command to bot's queue with timestamp
            command_entry = {
                "command": command,
                "timestamp": datetime.now().isoformat(),
                "status": "pending"
            }
            
            if 'params' in data:
                command_entry['params'] = data['params']
            
            bot_commands[bot_id].append(command_entry)
        
        logger.info(f"Command sent to bot {bot_id}: {command}")
        return jsonify({
            "status": "success",
            "message": f"Command sent to bot {bot_id}",
            "command": command
        })
        
    except Exception as e:
        logger.error(f"Error sending command: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/commands/<bot_id>', methods=['GET'])
def get_commands(bot_id: str):
    """Get pending commands for a specific bot."""
    try:
        with bot_lock:
            if bot_id not in bots:
                return jsonify({
                    "status": "error",
                    "message": f"Bot {bot_id} is not registered"
                }), 404
            
            # Update last seen timestamp
            bots[bot_id]['last_seen'] = datetime.now().isoformat()
            
            # Get pending commands
            pending_commands = bot_commands.get(bot_id, [])
            
        return jsonify({
            "status": "success",
            "bot_id": bot_id,
            "commands": pending_commands
        })
        
    except Exception as e:
        logger.error(f"Error getting commands for bot {bot_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/commands/<bot_id>/clear', methods=['POST'])
def clear_commands(bot_id: str):
    """Clear all commands for a specific bot."""
    try:
        with bot_lock:
            if bot_id not in bots:
                return jsonify({
                    "status": "error",
                    "message": f"Bot {bot_id} is not registered"
                }), 404
            
            cleared_count = len(bot_commands.get(bot_id, []))
            bot_commands[bot_id] = []
        
        logger.info(f"Cleared {cleared_count} commands for bot {bot_id}")
        return jsonify({
            "status": "success",
            "message": f"Cleared {cleared_count} commands for bot {bot_id}",
            "cleared_count": cleared_count
        })
        
    except Exception as e:
        logger.error(f"Error clearing commands for bot {bot_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/bots', methods=['GET'])
def list_bots():
    """Get a list of all registered bots."""
    try:
        with bot_lock:
            bot_list = []
            for bot_id, bot_data in bots.items():
                bot_info = {
                    "bot_id": bot_id,
                    "registered_at": bot_data.get('registered_at'),
                    "last_seen": bot_data.get('last_seen'),
                    "pending_commands": len(bot_commands.get(bot_id, []))
                }
                # Add other non-sensitive fields if they exist
                for field in ['name', 'version', 'status']:
                    if field in bot_data:
                        bot_info[field] = bot_data[field]
                
                bot_list.append(bot_info)
        
        return jsonify({
            "status": "success",
            "bots": bot_list,
            "total_count": len(bot_list)
        })
        
    except Exception as e:
        logger.error(f"Error listing bots: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/bots/<bot_id>', methods=['DELETE'])
def unregister_bot(bot_id: str):
    """Unregister a bot and clear its commands."""
    try:
        with bot_lock:
            if bot_id not in bots:
                return jsonify({
                    "status": "error",
                    "message": f"Bot {bot_id} is not registered"
                }), 404
            
            # Remove bot and its commands
            del bots[bot_id]
            if bot_id in bot_commands:
                del bot_commands[bot_id]
        
        logger.info(f"Bot {bot_id} unregistered successfully")
        return jsonify({
            "status": "success",
            "message": f"Bot {bot_id} unregistered successfully"
        })
        
    except Exception as e:
        logger.error(f"Error unregistering bot {bot_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"status": "error", "message": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting Flask bot management server...")
    logger.info("Available endpoints:")
    logger.info("  GET    /health - Health check")
    logger.info("  POST   /register - Register a bot")
    logger.info("  POST   /command - Send command to bot")
    logger.info("  GET    /commands/<bot_id> - Get pending commands")
    logger.info("  POST   /commands/<bot_id>/clear - Clear bot commands")
    logger.info("  GET    /bots - List all bots")
    logger.info("  DELETE /bots/<bot_id> - Unregister a bot")
    
    app.run(host='0.0.0.0', port=5000, debug=False)