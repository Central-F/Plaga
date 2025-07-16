# Bot Management Server API Documentation

This document describes the REST API endpoints for the Flask-based bot management server.

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the server is running and get basic statistics.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "registered_bots": 3
}
```

### 2. Register Bot
**POST** `/register`

Register a new bot or update existing bot information.

**Request Body:**
```json
{
  "bot_id": "bot_001",
  "name": "My Bot",
  "version": "1.0.0",
  "status": "active"
}
```

**Required Fields:**
- `bot_id`: Unique identifier for the bot

**Optional Fields:**
- `name`: Human-readable bot name
- `version`: Bot version
- `status`: Current bot status
- Any other custom fields

**Response (Success):**
```json
{
  "status": "success",
  "message": "Bot bot_001 registered successfully",
  "bot_id": "bot_001"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Missing required field: bot_id"
}
```

### 3. Send Command to Bot
**POST** `/command`

Send a command to a specific registered bot.

**Request Body:**
```json
{
  "bot_id": "bot_001",
  "command": "start_monitoring",
  "params": {
    "interval": 30,
    "target": "system_metrics"
  }
}
```

**Required Fields:**
- `bot_id`: ID of the target bot
- `command`: Command to execute

**Optional Fields:**
- `params`: Additional parameters for the command

**Response (Success):**
```json
{
  "status": "success",
  "message": "Command sent to bot bot_001",
  "command": "start_monitoring"
}
```

**Response (Error - Bot Not Found):**
```json
{
  "status": "error",
  "message": "Bot bot_001 is not registered"
}
```

### 4. Get Bot Commands
**GET** `/commands/<bot_id>`

Retrieve all pending commands for a specific bot.

**URL Parameters:**
- `bot_id`: ID of the bot

**Response (Success):**
```json
{
  "status": "success",
  "bot_id": "bot_001",
  "commands": [
    {
      "command": "start_monitoring",
      "timestamp": "2024-01-01T12:00:00.000000",
      "status": "pending",
      "params": {
        "interval": 30,
        "target": "system_metrics"
      }
    }
  ]
}
```

### 5. Clear Bot Commands
**POST** `/commands/<bot_id>/clear`

Clear all pending commands for a specific bot.

**URL Parameters:**
- `bot_id`: ID of the bot

**Response (Success):**
```json
{
  "status": "success",
  "message": "Cleared 3 commands for bot bot_001",
  "cleared_count": 3
}
```

### 6. List All Bots
**GET** `/bots`

Get a list of all registered bots with their information.

**Response:**
```json
{
  "status": "success",
  "bots": [
    {
      "bot_id": "bot_001",
      "name": "My Bot",
      "version": "1.0.0",
      "status": "active",
      "registered_at": "2024-01-01T11:00:00.000000",
      "last_seen": "2024-01-01T12:00:00.000000",
      "pending_commands": 2
    }
  ],
  "total_count": 1
}
```

### 7. Unregister Bot
**DELETE** `/bots/<bot_id>`

Remove a bot from the system and clear all its commands.

**URL Parameters:**
- `bot_id`: ID of the bot to unregister

**Response (Success):**
```json
{
  "status": "success",
  "message": "Bot bot_001 unregistered successfully"
}
```

## HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request data or missing required fields
- `404 Not Found`: Bot not found or invalid endpoint
- `405 Method Not Allowed`: HTTP method not supported for endpoint
- `500 Internal Server Error`: Server error

## Error Response Format

All error responses follow this format:
```json
{
  "status": "error",
  "message": "Description of the error"
}
```

## Bot Workflow Example

1. **Register a bot:**
   ```bash
   curl -X POST http://localhost:5000/register \
     -H "Content-Type: application/json" \
     -d '{"bot_id": "bot_001", "name": "Test Bot"}'
   ```

2. **Send commands to the bot:**
   ```bash
   curl -X POST http://localhost:5000/command \
     -H "Content-Type: application/json" \
     -d '{"bot_id": "bot_001", "command": "status_check"}'
   ```

3. **Bot polls for commands:**
   ```bash
   curl http://localhost:5000/commands/bot_001
   ```

4. **Bot clears processed commands:**
   ```bash
   curl -X POST http://localhost:5000/commands/bot_001/clear
   ```

## Security Considerations

- This server runs without authentication - implement proper authentication for production use
- All data is stored in memory and will be lost when the server restarts
- Consider adding rate limiting for production environments
- Add CORS headers if the API will be called from web browsers

## Threading and Concurrency

The server uses thread locks to ensure thread-safe operations when:
- Registering/unregistering bots
- Adding/retrieving/clearing commands
- Updating bot information

This makes the server safe for concurrent requests from multiple clients.