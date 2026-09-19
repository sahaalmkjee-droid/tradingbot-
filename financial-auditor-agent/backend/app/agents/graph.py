import logging
from typing import Dict, Any, Generator
from langgraph.graph import StateGraph, END
from app.agents.state import AuditorState
from app.agents.extractor import extractor_node
from app.agents.interpreter import interpreter_node
from app.agents.auditor import auditor_node
from app.agents.synthesizer import synthesizer_node

logger = logging.getLogger(__name__)

def build_auditor_graph():
    """Build and compile the multi-agent LangGraph workflow."""
    workflow = StateGraph(AuditorState)
    
    # Add Nodes
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("interpreter", interpreter_node)
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Set Entry Point & Edges
    workflow.set_entry_point("extractor")
    workflow.add_edge("extractor", "interpreter")
    workflow.add_edge("interpreter", "auditor")
    workflow.add_edge("auditor", "synthesizer")
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()

# Global compiled graph
auditor_app = build_auditor_graph()

def run_audit_workflow(ticker: str, horizon: str = "3-5 years", concern: str = "General", task_id: str = "") -> AuditorState:
    """Run the complete auditor graph synchronously."""
    initial_state: AuditorState = {
        "task_id": task_id,
        "ticker": ticker,
        "horizon": horizon,
        "concern": concern,
        "execution_logs": []
    }
    final_state = auditor_app.invoke(initial_state)
    return final_state

def stream_audit_workflow(ticker: str, horizon: str = "3-5 years", concern: str = "General", task_id: str = "") -> Generator[Dict[str, Any], None, None]:
    """Stream step events as each node executes in LangGraph."""
    initial_state: AuditorState = {
        "task_id": task_id,
        "ticker": ticker,
        "horizon": horizon,
        "concern": concern,
        "execution_logs": []
    }
    
    # Use stream mode to yield intermediate node events
    for event in auditor_app.stream(initial_state):
        for node_name, state_update in event.items():
            logs = state_update.get("execution_logs", [])
            latest_log = logs[-1] if logs else {"step": node_name, "message": f"Processing {node_name}..."}
            yield {
                "type": "step_update",
                "node": node_name,
                "log": latest_log,
                "partial_state": {
                    "company_name": state_update.get("company_name"),
                    "verified_ratios": state_update.get("verified_ratios"),
                    "health_scorecard": state_update.get("health_scorecard"),
                    "reality_checks": state_update.get("reality_checks"),
                    "risk_rules": state_update.get("risk_rules"),
                    "final_memo": state_update.get("final_memo")
                }
            }
