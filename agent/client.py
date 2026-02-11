"""
MCP HTTP client: encapsulates calls to the MCP server.
This client is defensive: the MCP server used in this workspace (FastMCP) may not provide
JSON REST endpoints at /api/*. To avoid UI errors, fall back to a safe mock response
when endpoints are missing or return errors.
"""
import httpx
from typing import Any, Dict

class McpClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(timeout=timeout)

    def fetch_state(self) -> Dict[str, Any]:
        """Fetch latest state from MCP server. If the server returns 404 or other errors,
        return a safe mock structure so the UI doesn't crash."""
        url = f"{self.base_url}/api/state"
        try:
            resp = self.client.get(url)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            # endpoint not present or server returns non-2xx
            return {"_mock": True, "error": f"server returned {e.response.status_code} for {url}", "state": {}}
        except Exception as e:
            return {"_mock": True, "error": str(e), "state": {}}

    def fetch_records(self, limit: int = 10) -> Dict[str, Any]:
        url = f"{self.base_url}/api/records?limit={limit}"
        try:
            resp = self.client.get(url)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            return {"_mock": True, "error": f"server returned {e.response.status_code} for {url}", "records": []}
        except Exception as e:
            return {"_mock": True, "error": str(e), "records": []}

    def post_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/action"
        try:
            resp = self.client.post(url, json={"action": action, "payload": payload})
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"_mock": True, "error": str(e), "result": None}
