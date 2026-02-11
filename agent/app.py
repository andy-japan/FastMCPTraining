"""
Entrypoint for the agent. Provides a simple CLI and a FastAPI endpoint for demo.
"""
import argparse
import os
from client import McpClient
from langgraph_flow import AgentGraph

# LLM wrapper: use langchain/OpenAI-compatible endpoint if configured
from llm import make_llm

class SimpleLLM:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        try:
            self._impl = make_llm(model=model, temperature=temperature)
        except Exception:
            # Fallback to a trivial mock if external LLM is not available
            self._impl = None

    def generate(self, prompt: str) -> str:
        if self._impl is None:
            return "[LLM simulated response] Short assessment based on prompt length: " + str(len(prompt))
        return self._impl.generate(prompt)


def run_once(mcp_url: str):
    """コマンドラインから 1 回だけ実行するエントリポイント（デバッグ用）"""
    mcp = McpClient(mcp_url)
    llm = SimpleLLM()
    ag = AgentGraph(mcp, llm)
    out = ag.run()
    print("Agent output:\n", out)


def serve_streamlit():
    """Streamlit を起動するためのラッパー（docker では streamlit run を使う想定）"""
    # streamlit は別プロセスで起動するためここでは参照のみ
    print('Streamlit UI は streamlit run agent/ui/streamlit_app.py で起動してください')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mcp-url', default=os.environ.get('MCP_URL','http://localhost:8000'), help='MCP server base URL')
    parser.add_argument('--serve', action='store_true', help='Streamlit サーバー表示用フラグ')
    args = parser.parse_args()
    if args.serve:
        serve_streamlit()
    else:
        run_once(args.mcp_url)
