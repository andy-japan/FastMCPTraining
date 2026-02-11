"""
Entrypoint for the agent. Provides a simple CLI and a FastAPI endpoint for demo.
"""
import argparse
import os
from client import McpClient
from langgraph_flow import AgentGraph

# Placeholder LLM wrapper
class SimpleLLM:
    def __init__(self):
        pass
    def generate(self, prompt: str) -> str:
        # In real use, replace with OpenAI/Local LLM call
        return "[LLM simulated response] Short assessment based on prompt length: " + str(len(prompt))


def run_once(mcp_url: str):
    mcp = McpClient(mcp_url)
    llm = SimpleLLM()
    ag = AgentGraph(mcp, llm)
    out = ag.run()
    print("Agent output:\n", out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mcp-url', default=os.environ.get('MCP_URL','http://localhost:8000'), help='MCP server base URL')
    args = parser.parse_args()
    run_once(args.mcp_url)
