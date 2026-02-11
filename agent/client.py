"""
MCP HTTP client: encapsulates calls to the MCP server.
"""
import httpx
from typing import Any, Dict

class McpClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(timeout=timeout)

    def fetch_state(self) -> Dict[str, Any]:
        """Fetch latest state from MCP server."""
        url = f"{self.base_url}/api/state"
        resp = self.client.get(url)
        resp.raise_for_status()
        return resp.json()

    def fetch_records(self, limit: int = 10) -> Dict[str, Any]:
        url = f"{self.base_url}/api/records?limit={limit}"
        resp = self.client.get(url)
        resp.raise_for_status()
        return resp.json()

    def post_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/action"
        resp = self.client.post(url, json={"action": action, "payload": payload})
        resp.raise_for_status()
        return resp.json()
