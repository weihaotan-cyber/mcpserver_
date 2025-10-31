from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# ---- integrate third-party MCP servers via a proxy config
third_party = FastMCP.as_proxy({
    "mcpServers": {
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest", "--isolated"]
        },
        # "fs": {
        #     "command": "npx",
        #     "args": [
        #         "-y",
        #         "@modelcontextprotocol/server-filesystem", 
        #         "/Users/weihao/Desktop/llm"]
        # }
    }
}, name="ThirdParty")

# Mount them so everything appears under one server
# Tools/resources will be auto-prefixed by their config names: playwright_..., fs_...
mcp.mount(third_party)

if __name__ == "__main__":
    mcp.run(transport="http", port=8002)