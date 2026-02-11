"""
LangGraph flow definition (example). Uses LangChain/LangGraph style pseudo-API.
This file defines a simple graph: fetch -> summarize -> reason -> output
"""
# エージェントのビジネスロジック層：LangGraph フロー定義
# このモジュールは処理の流れ（取得→要約→推論→出力）を定義します。
# LLM は外部から注入（引数 llm）し、テスト時はモックに差し替えられます。

from processor import summarize_state, extract_recent_events
from client import McpClient

try:
    # LangGraph が利用可能であれば取り込む（デフォルトの雛形用）
    from langgraph import Graph, Node
except Exception:
    # LangGraph がない環境でも動くように簡易なモック実装を提供
    class Graph:
        def __init__(self, name=None):
            self.name = name
            self.nodes = []
            self.edges = []
        def add_nodes(self, nodes):
            self.nodes.extend(nodes)
        def connect(self, a, b):
            self.edges.append((a,b))
        def run(self, inp):
            # 単純な直列実行を行う
            data = {}
            for n in self.nodes:
                data = n.func(data)
            return data
    class Node:
        def __init__(self, func):
            self.func = func

class AgentGraph:
    def __init__(self, mcp: McpClient, llm):
        """コンストラクタ
        mcp: MCP 接続用クライアント
        llm: LLM ラッパー（generate メソッドを持つオブジェクト）
        """
        self.mcp = mcp
        self.llm = llm
        self.graph = Graph(name="mcp-agent-graph")
        self._build()

    def _build(self):
        # ノードを定義してグラフに追加する
        fetch_node = Node(func=self._fetch)
        summarize_node = Node(func=self._summarize)
        reason_node = Node(func=self._reason)
        output_node = Node(func=self._output)

        self.graph.add_nodes([fetch_node, summarize_node, reason_node, output_node])
        self.graph.connect(fetch_node, summarize_node)
        self.graph.connect(summarize_node, reason_node)
        self.graph.connect(reason_node, output_node)

    def _fetch(self, input_):
        """MCP から状態とレコードを取得する。クライアントがフォールバック（mock）を返す場合に備えて正規化する。"""
        state_resp = self.mcp.fetch_state()
        records_resp = self.mcp.fetch_records(limit=10)
        # Unwrap defensive client responses which may include wrappers like {"_mock": True, "state": {...}}
        if isinstance(state_resp, dict) and 'state' in state_resp:
            state = state_resp.get('state', {})
        else:
            state = state_resp if isinstance(state_resp, dict) else {}
        if isinstance(records_resp, dict) and 'records' in records_resp:
            records = records_resp.get('records', [])
        else:
            # If it's already a list, keep it; if it's a dict fallback to empty list
            records = records_resp if isinstance(records_resp, list) else []
        return {"state": state, "records": records}

    def _summarize(self, data):
        """取得データを要約する（入力が想定外でも安全に処理する）"""
        state = data.get('state', {}) or {}
        records = data.get('records', []) or []
        # Ensure types
        if not isinstance(state, dict):
            state = {}
        if not isinstance(records, list):
            records = []
        s = summarize_state(state)
        events = extract_recent_events(records)
        return {"summary": s, "events": events}

    def _reason(self, data):
        """要約と最近のイベントを元に LLM へプロンプトを送り、評価を得る"""
        prompt = "次のシステム状態と最近のイベントに基づき、短い評価を返してください:\n"
        prompt += data['summary'] + "\n最近のイベント:\n" + "\n".join(data['events'])
        # LLM 呼び出し。llm.generate を想定
        if self.llm is None:
            return {"assessment": "[LLM 未設定]"}
        resp = self.llm.generate(prompt)
        return {"assessment": resp}

    def _output(self, data):
        """最終的な出力を返す"""
        return data.get('assessment')

    def run(self):
        """グラフを実行して結果を返す"""
        return self.graph.run({})
