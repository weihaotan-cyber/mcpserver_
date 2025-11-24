from fastmcp import FastMCP
# from fastmcp.utilities.httpx_sse import ServerSentEvent
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import os
from typing import Optional
from dotenv import load_dotenv
from authlib.jose import jwt
from authlib.jose.errors import JoseError
import httpx
import asyncio
import secrets
from fastmcp.server.auth.providers.google import GoogleProvider

# Load environment variables from .env file
load_dotenv()


ISSUER = os.getenv("OIDC_ISSUER", "").rstrip('/')
CLIENT_ID = os.getenv("OIDC_CLIENT_ID")
CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET")
REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI", "http://localhost:8000/callback")
SESSION_SECRET = os.getenv("SESSION_SECRET", secrets.token_urlsafe(32))

auth_provider = GoogleProvider(
    client_id=CLIENT_ID,  
    client_secret=CLIENT_SECRET,
    base_url="https://pseudohemal-unexigent-brayan.ngrok-free.dev",                 
    required_scopes=[                               
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    # redirect_path=REDIRECT_URI              
)

mcp = FastMCP(
    "My MCP Server",
    # auth=auth_provider
)

@mcp.tool(
    name="get_conversations",
    description="Get a list of all conversations (overview/summary). Use this to see all available conversations. Requires an access token - use the authorize_user tool first to obtain the token, then pass the 'token' field from its response to this tool. For details of a specific conversation, use get_conversation_details instead.", 
)
async def get_conversations(token:str, page: int = 1, limit: int = 10, sort: str = "created_by", order: str = "DESC") -> dict:
    """Internal function description (ignored if description is provided above)."""

    async with httpx.AsyncClient() as client:
        try:
            params = {
                "page": page,
                "limit": limit,
                "sort": sort,
                "order": order
            }
                     
            response = await client.get(
                "https://odin-gpt.ai-momentum.com/chatbot/api/chats/conversations",
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }

@mcp.tool(
    name="get_conversation_details",
    description="Get detailed information about a SPECIFIC conversation by its ID. Use this when you need the full content/messages of a particular conversation. You must provide the ID. Requires an access token - use the authorize_user tool first to obtain the token, then pass the 'token' field from its response to this tool. To get a list of all conversations first, use get_conversations.", 
)
async def get_conversation_details(token: str, id: str, page: int = 1, limit: int = 10, sort: str = "created_by", order: str = "DESC") -> dict:
    """Internal function description (ignored if description is provided above)."""

    async with httpx.AsyncClient() as client:
        try:
            params = {
                "page": page,
                "limit": limit,
                "sort": sort,
                "order": order
            }
                     
            response = await client.get(
                f"https://odin-gpt.ai-momentum.com/chatbot/api/chats/conversations/{id}",
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }


@mcp.tool(    
    enabled=False
)
async def get_user_info() -> dict:
    """Returns information about the authenticated Google user."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()
    # The GoogleProvider stores user data in token claims
    return {
        "google_id": token.claims.get("sub"),
        "email": token.claims.get("email"),
        "name": token.claims.get("name"),
        "picture": token.claims.get("picture"),
        "locale": token.claims.get("locale"),
        "token":token
    }

@mcp.tool(
    name="authorize_user",
    description="Authorize and get information about the authenticated user.", 
)
async def authorize_user(user_id: str,channel: str,entry_point: str,language: str) -> dict:
    """Returns information about the authenticated user."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://odin-gpt.ai-momentum.com/chatbot/api/tokens/generate",
                json={
                    "user_id": user_id,
                    "channel": channel,
                    "entry_point": entry_point,
                    "language": language
                },
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": "secret"
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }


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
# mcp.mount(third_party)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)