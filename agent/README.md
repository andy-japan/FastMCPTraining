LangGraph-based AI agent for FastMCPTraining

This folder contains an AI agent that connects to the FastMCPTraining MCP server, fetches data and performs simple reasoning using LangGraph.

Design principles:
- Do not modify the original MCP server source.
- Keep code modular: client, processing, langgraph flow, entrypoint.
- Provide Docker support and docker-compose service addition.

Files:
- agent/client.py  # MCP HTTP client
- agent/processor.py  # data processing utilities
- agent/langgraph_flow.py  # LangGraph graph definition
- agent/app.py  # CLI/web entrypoint
- agent/Dockerfile
- agent/requirements.txt
- agent/docker-compose.agent.yml  # optional compose fragment to include service

Usage (local dev):
- python3 -m venv .venv
- . .venv/bin/activate
- pip install -r requirements.txt
- python app.py --mcp-url http://mcp-server:8000

Note: push destination will be provided later; this code will be kept local until instructed to push.