# MCP Server Setup

This project is an MCP (Model Context Protocol) server using FastMCP.

## Features
- Custom tool: `greet(name: str)`
- Integration with third-party MCP servers (e.g., Playwright) via proxy config
- HTTP server on port 8002

## Prerequisites
- Python 3.12+
- Node.js (for third-party MCP servers via npx)
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

   If not already installed, run:
   ```zsh
   pip install fastmcp
   ```

4. **(Optional) Install third-party MCP servers**

   For Playwright MCP server:
   ```zsh
   npx @playwright/mcp@latest --isolated
   ```
   For other servers, update the proxy config in `server.py` as needed.

## Usage

Start the MCP server:

```zsh
python server.py
```

The server will run on `http://localhost:8002`.

## Customization
- Add new tools by decorating functions with `@mcp.tool` in `server.py`.
- Integrate more MCP servers by editing the `third_party` proxy config.

## File Overview
- `server.py`: Main server code and configuration
- `bin/activate`: Virtual environment activation script
- `lib/python3.12/site-packages/`: Installed Python packages

## License
Specify your license here.
