# Bot Management Server

A Flask-based REST API server for managing and controlling remote bots. This system allows you to register bots, send commands to them, and track their status.

## Features

- **Bot Registration**: Register bots with custom metadata
- **Command Queue**: Send commands to specific bots with parameters
- **Health Monitoring**: Track bot registration time and last seen status
- **Thread-Safe**: Concurrent request handling with proper locking
- **Error Handling**: Comprehensive error handling and validation
- **Logging**: Detailed logging for debugging and monitoring

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python server_improved.py
```

The server will start on `http://localhost:5000`

### 3. Test the Server

Run the test script to verify all endpoints:

```bash
python test_server.py
```

### 4. Run Example Bot

In another terminal, start the example bot client:

```bash
python example_bot_client.py
```

## Files Description

- **`server.py`** - Original basic server implementation
- **`server_improved.py`** - Enhanced server with full features
- **`test_server.py`** - Comprehensive test suite for all endpoints
- **`example_bot_client.py`** - Example bot that demonstrates client-side implementation
- **`requirements.txt`** - Python dependencies
- **`API_DOCUMENTATION.md`** - Complete API documentation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health check |
| POST | `/register` | Register a new bot |
| POST | `/command` | Send command to bot |
| GET | `/commands/<bot_id>` | Get pending commands |
| POST | `/commands/<bot_id>/clear` | Clear bot commands |
| GET | `/bots` | List all registered bots |
| DELETE | `/bots/<bot_id>` | Unregister a bot |

## Usage Examples

### Register a Bot

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "my_bot_001",
    "name": "My First Bot",
    "version": "1.0.0",
    "status": "active"
  }'
```

### Send a Command

```bash
curl -X POST http://localhost:5000/command \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "my_bot_001",
    "command": "start_monitoring",
    "params": {
      "interval": 30,
      "target": "cpu_usage"
    }
  }'
```

### Get Bot Commands

```bash
curl http://localhost:5000/commands/my_bot_001
```

## Bot Client Implementation

The example bot client (`example_bot_client.py`) demonstrates how to:

1. Register with the server
2. Poll for commands periodically  
3. Execute commands based on type
4. Clear processed commands
5. Handle graceful shutdown

### Basic Bot Loop

```python
# Register bot
bot.register()

# Main loop
while running:
    # Poll for commands
    commands = bot.poll_commands()
    
    # Execute commands
    for command in commands:
        bot.execute_command(command)
    
    # Clear processed commands
    bot.clear_commands()
    
    # Wait before next poll
    time.sleep(poll_interval)
```

## Architecture

### Server Components

- **Flask Web Server**: Handles HTTP requests
- **In-Memory Storage**: Stores bot data and command queues
- **Thread Locks**: Ensures thread-safe operations
- **Logging**: Tracks all operations and errors

### Data Models

**Bot Registration:**
```json
{
  "bot_id": "unique_identifier",
  "name": "Human readable name",
  "version": "1.0.0",
  "status": "active",
  "registered_at": "2024-01-01T12:00:00.000000",
  "last_seen": "2024-01-01T12:05:00.000000"
}
```

**Command Structure:**
```json
{
  "command": "command_name",
  "timestamp": "2024-01-01T12:00:00.000000",
  "status": "pending",
  "params": {
    "key": "value"
  }
}
```

## Security Considerations

⚠️ **Important**: This is a basic implementation for development/testing purposes.

For production use, consider adding:

- **Authentication**: API keys or OAuth
- **Authorization**: Role-based access control
- **HTTPS**: SSL/TLS encryption
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Sanitize all inputs
- **Persistent Storage**: Database instead of memory
- **Monitoring**: Health checks and metrics

## Development

### Running Tests

```bash
# Start server in one terminal
python server_improved.py

# Run tests in another terminal
python test_server.py
```

### Adding New Commands

1. Add command handling in bot client's `execute_command()` method
2. Update server validation if needed
3. Test the new command flow

### Extending the Server

- Add authentication middleware
- Implement persistent storage
- Add WebSocket support for real-time communication
- Create a web dashboard for bot management

## Troubleshooting

**Connection Refused:**
- Ensure the server is running on port 5000
- Check firewall settings

**Bot Not Registered:**
- Check bot registration response
- Verify bot_id is unique and valid

**Commands Not Received:**
- Check bot polling interval
- Verify bot is calling the correct endpoint
- Check server logs for errors

## License

This project is for educational and development purposes.