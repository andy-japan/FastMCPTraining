# Minimal Streamlit UI: only keep the "推論を実行" button as requested
# Ensure parent package path is on PYTHONPATH so imports work
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
from client import McpClient
from langgraph_flow import AgentGraph

st.title('MCP エージェント デモ')
st.write('推論ボタンのみを表示します。')

# Fixed MCP URL (hidden)
mcp_url = 'http://mcp-server:8000'

st.subheader('簡易推論')
if st.button('推論を実行'):
    client = McpClient(mcp_url)
    try:
        # Use SimpleLLM from app as a mock LLM
        from app import SimpleLLM
        ag = AgentGraph(client, SimpleLLM())
        result = ag.run()
        if isinstance(result, dict):
            out = result.get('assessment') or result
        else:
            out = result
        st.subheader('推論結果')
        st.write(out)
    except Exception as e:
        st.error(f'推論エラー: {e}')
