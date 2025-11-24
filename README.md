# MCP Server Setup

This project is an MCP (Model Context Protocol) server using FastMCP that provides conversation management tools for the Odin GPT API.

## Features
- **User Authorization**: `authorize_user` - Generate access tokens for API authentication
- **Conversation Management**: 
  - `get_conversations` - Retrieve paginated list of all conversations
  - `get_conversation_details` - Get detailed information about specific conversations
- Optional integration with third-party MCP servers (e.g., Playwright) via proxy config
- HTTP server on port 8000

## Prerequisites
- Python 3.12+
- Node.js (for third-party MCP servers via npx, if enabled)
- Recommended: Use the provided virtual environment

## Installation

1. **Clone the repository**

   ```zsh
   git clone <your-repo-url>
   cd mcpserver
   ```

2. **Activate the Python virtual environment**

   ```zsh
   source bin/activate
   ```

3. **Install required Python packages**

   ```zsh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root with the following variables:
   ```
   OIDC_ISSUER=<your-oidc-issuer>
   OIDC_CLIENT_ID=<your-client-id>
   OIDC_CLIENT_SECRET=<your-client-secret>
   OIDC_REDIRECT_URI=http://localhost:8000/callback
   SESSION_SECRET=<your-session-secret>
   ```

5. **(Optional) Install third-party MCP servers**

   For Playwright MCP server:
   ```zsh
   npx @playwright/mcp@latest --isolated
   ```
   
   Uncomment the `mcp.mount(third_party)` line in `server.py` to enable.

## Usage

Start the MCP server:

```zsh
python server.py
```

The server will run on `http://localhost:8000`.

## Available Tools

### `authorize_user`
Generates an access token for API authentication.

**Parameters:**
- `user_id` (str): User identifier
- `channel` (str): Communication channel (e.g., "agency")
- `entry_point` (str): Entry point identifier
- `language` (str): Language code (e.g., "en")

**Returns:** Dictionary containing the access token

### `get_conversations`
Retrieves a paginated list of conversations.

**Parameters:**
- `token` (str): Access token from `authorize_user`
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 10)
- `sort` (str, optional): Sort field (default: "created_by")
- `order` (str, optional): Sort order "ASC" or "DESC" (default: "DESC")

**Returns:** Dictionary with conversation list and metadata

### `get_conversation_details`
Gets detailed information about a specific conversation.

**Parameters:**
- `token` (str): Access token from `authorize_user`
- `id` (str): Conversation ID
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 10)
- `sort` (str, optional): Sort field (default: "created_by")
- `order` (str, optional): Sort order "ASC" or "DESC" (default: "DESC")

**Returns:** Dictionary with conversation details and messages

## Customization
- Add new tools by decorating functions with `@mcp.tool` in `server.py`
- Integrate more MCP servers by editing the `third_party` proxy config
- Modify API endpoints in the tool functions as needed

## File Overview
- `server.py`: Main server code and tool definitions
- `requirements.txt`: Python package dependencies
- `bin/activate`: Virtual environment activation script
- `lib/python3.12/site-packages/`: Installed Python packages
- `.env`: Environment configuration (create this file)

## API Integration
The server integrates with the Odin GPT API at `https://odin-gpt.ai-momentum.com/chatbot/api/`

## License
Specify your license here.
