import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from tidio_client import TidioApiClient

load_dotenv()

mcp = FastMCP("Tidio")

tidio_api_client = TidioApiClient(
    client_id=os.getenv("TIDIO_CLIENT_ID", ""),
    client_secret=os.getenv("TIDIO_CLIENT_SECRET", ""),
)


def _tool_call_succeed(data: dict = None) -> dict:
    return {
        "status": "ok",
        "data": data or {},
    }
