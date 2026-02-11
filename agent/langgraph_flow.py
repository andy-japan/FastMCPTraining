"""
LangGraph flow definition (example). Uses LangChain/LangGraph style pseudo-API.
This file defines a simple graph: fetch -> summarize -> reason -> output
"""
from langgraph import Graph, Node
from processor import summarize_state, extract_recent_events
from client import McpClient

# NOTE: exact LangGraph API may differ; this is a representative structure.

class AgentGraph:
    def __init__(self, mcp: McpClient, llm):
        self.mcp = mcp
        self.llm = llm
        self.graph = Graph(name="mcp-agent-graph")
        self._build()

    def _build(self):
        # Nodes
        fetch_node = Node(func=self._fetch)
        summarize_node = Node(func=self._summarize)
        reason_node = Node(func=self._reason)
        output_node = Node(func=self._output)

        # Connect nodes
        self.graph.add_nodes([fetch_node, summarize_node, reason_node, output_node])
        self.graph.connect(fetch_node, summarize_node)
        self.graph.connect(summarize_node, reason_node)
        self.graph.connect(reason_node, output_node)

    def _fetch(self, input_):
        state = self.mcp.fetch_state()
        records = self.mcp.fetch_records(limit=10)
        return {"state": state, "records": records}

    def _summarize(self, data):
        state = data['state']
        records = data['records']
        s = summarize_state(state)
        events = extract_recent_events(records)
        return {"summary": s, "events": events}

    def _reason(self, data):
        prompt = "Based on the following state and recent events, provide a short assessment:\n"
        prompt += data['summary'] + "\nRecent events:\n" + "\n".join(data['events'])
        # call LLM
        resp = self.llm.generate(prompt)
        return {"assessment": resp}

    def _output(self, data):
        return data['assessment']

    def run(self):
        return self.graph.run({})
