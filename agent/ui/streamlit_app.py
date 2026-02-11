# Streamlit アプリケーション（UI 層）
# このファイルは UI（プレゼンテーション層）に属し、内部ロジックは別モジュールから呼び出します。

# Ensure parent package path is on PYTHONPATH so imports like `from client import ...` work
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
from client import McpClient
from processor import summarize_state, extract_recent_events
from langgraph_flow import AgentGraph

# 日本語の説明と簡単な操作パネルを実装
st.title('MCP エージェント デモ')
st.write('MCP サーバーからデータを取得して要約・推論を行うデモ UI です。')

# Use fixed MCP URL (do not show editable URL per request)
mcp_url = 'http://mcp-server:8000'

if 'agent' not in st.session_state:
    st.session_state.agent = None

col1, col2 = st.columns(2)

with col1:
    if st.button('最新ステートを取得'):
        client = McpClient(mcp_url)
        state = client.fetch_state()
        st.session_state['state'] = state
        if state.get('_mock'):
            st.warning('サーバが期待する REST API を提供していないため、モックデータを返しました。詳細: ' + str(state.get('error')))
        else:
            st.success('取得成功')

with col2:
    if st.button('最近のレコードを取得'):
        client = McpClient(mcp_url)
        records = client.fetch_records(limit=10)
        st.session_state['records'] = records
        if records.get('_mock'):
            st.warning('サーバが期待する REST API を提供していないため、モックデータを返しました。詳細: ' + str(records.get('error')))
        else:
            st.success('取得成功')

# 表示エリア
if 'state' in st.session_state:
    st.subheader('ステート要約')
    try:
        st.text(summarize_state(st.session_state['state'].get('state', st.session_state['state'])))
    except Exception:
        st.text(str(st.session_state['state']))

if 'records' in st.session_state:
    st.subheader('最近のイベント')
    recs = st.session_state['records'].get('records', st.session_state['records'])
    try:
        events = extract_recent_events(recs, limit=10)
        for ev in events:
            st.write(ev)
    except Exception:
        st.write(recs)

# 簡易推論ボタン（LLMはモック）
st.subheader('簡易推論')
if st.button('推論を実行'):
    client = McpClient(mcp_url)
    try:
        # Build agent and supply a SimpleLLM if none provided
        from app import SimpleLLM
        ag = AgentGraph(client, SimpleLLM())
        result = ag.run()
        # AgentGraph.run may return dict or string; normalize
        if isinstance(result, dict):
            out = result.get('assessment') or result
        else:
            out = result
        st.subheader('推論結果')
        st.write(out)
    except Exception as e:
        st.error(f'推論エラー: {e}')
