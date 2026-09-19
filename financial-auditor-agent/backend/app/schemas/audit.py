from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AuditRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g. AAPL, NVDA, TSLA, MSFT)")
    horizon: str = Field("3-5 years", description="Target investment horizon")
    concern: str = Field("General", description="Primary investor concern or focus area")

class HealthScorecardItem(BaseModel):
    id: str
    title: str
    status: str  # 'green' | 'yellow' | 'red'
    value: str
    detail: str

class RealityCheckItem(BaseModel):
    id: str
    topic: str
    claim: str
    reality: str
    takeaway: str

class RiskRule(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # 'high' | 'medium' | 'low'

class AuditResponse(BaseModel):
    task_id: str
    ticker: str
    company_name: str
    horizon: str
    concern: str
    verified_ratios: Dict[str, Any]
    health_scorecard: List[HealthScorecardItem]
    reality_checks: List[RealityCheckItem]
    risk_rules: List[RiskRule]
    final_memo: str
    execution_logs: List[Dict[str, Any]]
