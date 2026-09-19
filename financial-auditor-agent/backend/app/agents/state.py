from typing import TypedDict, List, Dict, Any, Optional

class AuditorState(TypedDict, total=False):
    task_id: str
    ticker: str
    horizon: str
    concern: str
    company_name: str
    raw_filing_facts: Dict[str, Any]
    code_to_run: str
    verified_ratios: Dict[str, Any]
    execution_logs: List[Dict[str, Any]]
    anomalies: List[Dict[str, Any]]
    health_scorecard: List[Dict[str, Any]]
    reality_checks: List[Dict[str, Any]]
    risk_rules: List[Dict[str, Any]]
    final_memo: str
