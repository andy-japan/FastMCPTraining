"""
Processing utilities for MCP data prior to sending to LangGraph
"""
from typing import Dict, Any, List

def summarize_state(state: Dict[str, Any]) -> str:
    # Simple summarization for demo purposes
    lines = []
    for k, v in state.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)

def extract_recent_events(records: List[Dict[str, Any]], limit: int = 5) -> List[str]:
    events = []
    for r in records[:limit]:
        t = r.get('timestamp', '')
        d = r.get('detail', '')
        events.append(f"{t} - {d}")
    return events
