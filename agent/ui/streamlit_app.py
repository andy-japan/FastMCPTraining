# Streamlit アプリケーション（UI 層）
# このファイルは UI（プレゼンテーション層）に属し、内部ロジックは別モジュールから呼び出します。

import streamlit as st
from client import McpClient
from processor import summarize_state, extract_recent_events
from langgraph_flow import AgentGraph

# 日本語の説明と簡単な操作パネルを実装
st.title('MCP エージェント デモ')
st.write('MCP サーバーからデータを取得して要約・推論を行うデモ UI です。')

mcp_url = st.text_input('MCP サーバー URL', value='http://mcp-server:8000')

if 'agent' not in st.session_state:
    st.session_state.agent = None

col1, col2 = st.columns(2)

with col1:
    if st.button('最新ステートを取得'):
        try:
            client = McpClient(mcp_url)
            state = client.fetch_state()
            st.session_state['state'] = state
            st.success('取得成功')
        except Exception as e:
            st.error(f'取得エラー: {e}')

with col2:
    if st.button('最近のレコードを取得'):
        try:
            client = McpClient(mcp_url)
            records = client.fetch_records(limit=10)
            st.session_state['records'] = records
            st.success('取得成功')
        except Exception as e:
            st.error(f'取得エラー: {e}')

# 表示エリア
if 'state' in st.session_state:
    st.subheader('ステート要約')
    st.text(summarize_state(st.session_state['state']))

if 'records' in st.session_state:
    st.subheader('最近のイベント')
    events = extract_recent_events(st.session_state['records'], limit=10)
    for ev in events:
        st.write(ev)

# 簡易推論ボタン（LLMはモック）
st.subheader('簡易推論')
if st.button('推論を実行'):
    try:
        client = McpClient(mcp_url)
        llm = None
        ag = AgentGraph(client, llm)
        # AgentGraph の _reason は内部で llm.generate を呼ぶため、モックとして SimpleLLM を使う
        from app import SimpleLLM
        ag.llm = SimpleLLM()
        result = ag.run()
        st.subheader('推論結果')
        st.write(result)
    except Exception as e:
        st.error(f'推論エラー: {e}')
