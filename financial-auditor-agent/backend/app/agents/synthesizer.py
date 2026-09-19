import datetime
import logging
from app.agents.state import AuditorState

logger = logging.getLogger(__name__)

def synthesizer_node(state: AuditorState) -> AuditorState:
    logs = state.get("execution_logs", [])
    ticker = state.get("ticker", "AAPL").upper()
    company = state.get("company_name", ticker)
    ratios = state.get("verified_ratios", {})
    anomalies = state.get("anomalies", [])
    horizon = state.get("horizon", "3-5 years")
    
    logs.append({
        "step": "Synthesizer",
        "message": f"Formulating institutional Executive Dossier & Health Scorecard for {company} ({ticker})...",
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    # 1. Health Scorecard Construction
    cash = ratios.get("cash", 0)
    lt_debt = ratios.get("lt_debt", 0)
    debt_eq = ratios.get("debt_to_equity", 0.0)
    accruals = ratios.get("accruals_ratio", 0.0)
    fcf = ratios.get("free_cash_flow", 0.0)
    cash_conv = ratios.get("cash_conversion_quality", 1.0)
    bs_balanced = ratios.get("bs_balanced", True)
    
    # Card 1: Cash vs Debt
    if lt_debt == 0 or cash > lt_debt:
        cash_status = "green"
        cash_title = "Pristine Balance Sheet"
        cash_val = f"${cash/1e9:.2f}B Cash vs ${lt_debt/1e9:.2f}B Debt"
        cash_detail = f"Net cash positive position with low default risk."
    elif debt_eq < 1.2:
        cash_status = "green"
        cash_title = "Manageable Leverage"
        cash_val = f"D/E Ratio: {debt_eq:.2f}x"
        cash_detail = f"Debt is well supported by current asset coverage."
    else:
        cash_status = "yellow" if debt_eq < 2.5 else "red"
        cash_title = "Elevated Leverage"
        cash_val = f"D/E Ratio: {debt_eq:.2f}x"
        cash_detail = f"Debt burden requires sustained operating cash flow."

    # Card 2: Earnings Quality
    if abs(accruals) < 0.05 and cash_conv >= 0.8:
        eq_status = "green"
        eq_title = "High Earnings Quality"
        eq_val = f"Sloan Accruals: {accruals:.4f}"
        eq_detail = "Reported earnings are backed by hard cash collections."
    elif abs(accruals) < 0.10:
        eq_status = "yellow"
        eq_title = "Moderate Accruals"
        eq_val = f"Sloan Accruals: {accruals:.4f}"
        eq_detail = "Minor non-cash accounting adjustments detected."
    else:
        eq_status = "red"
        eq_title = "Aggressive Accruals"
        eq_val = f"Sloan Accruals: {accruals:.4f}"
        eq_detail = "High proportion of net income comes from non-cash accounting."

    # Card 3: Working Capital & Cash Generation
    if fcf > 0:
        wc_status = "green"
        wc_title = "Positive Free Cash Flow"
        wc_val = f"${fcf/1e9:.2f}B Annual FCF"
        wc_detail = "Sufficient cash flow remaining after capital expenditure."
    else:
        wc_status = "yellow"
        wc_title = "Negative Free Cash Flow"
        wc_val = f"${fcf/1e9:.2f}B Annual FCF"
        wc_detail = "Capital expenditure consumes full operating cash flow."

    # Card 4: Overall Verdict
    red_count = sum(1 for s in [cash_status, eq_status, wc_status] if s == "red")
    yellow_count = sum(1 for s in [cash_status, eq_status, wc_status] if s == "yellow")
    
    if red_count == 0 and yellow_count <= 1 and bs_balanced:
        verdict_status = "green"
        verdict_title = "APPROVED - STRONG VITALS"
        verdict_val = "Clean Quantitative Audit"
        verdict_detail = f"Audited statements confirm high mathematical balance and cash alignment over {horizon} horizon."
    elif red_count >= 2 or not bs_balanced:
        verdict_status = "red"
        verdict_title = "HIGH AUDIT CAUTION"
        verdict_val = "Significant Discrepancies"
        verdict_detail = "Quantitative red flags detected in cash flow conversion or balance sheet integrity."
    else:
        verdict_status = "yellow"
        verdict_title = "MODERATE MONITORING"
        verdict_val = "Satisfactory Vitals"
        verdict_detail = f"Acceptable fundamental base, but monitor debt levels and working capital trends."

    health_scorecard = [
        {"id": "cash_debt", "title": "Cash vs Debt", "status": cash_status, "value": cash_val, "detail": cash_detail},
        {"id": "earnings_quality", "title": "Earnings Quality", "status": eq_status, "value": eq_val, "detail": eq_detail},
        {"id": "working_capital", "title": "Free Cash Flow", "status": wc_status, "value": wc_val, "detail": wc_detail},
        {"id": "verdict", "title": "Executive Verdict", "status": verdict_status, "value": verdict_val, "detail": verdict_detail}
    ]

    # 2. Reality Check Matrix Formatting
    reality_checks = []
    for idx, item in enumerate(anomalies):
        reality_checks.append({
            "id": f"rc_{idx+1}",
            "topic": item.get("topic", f"Check {idx+1}"),
            "claim": item.get("claim", ""),
            "reality": item.get("reality", ""),
            "takeaway": item.get("takeaway", "")
        })

    # 3. 3 Actionable Rules Before Buying
    risk_rules = [
        {
            "id": "rule_1",
            "title": "Verify Free Cash Flow vs Net Income",
            "description": f"Always confirm that Operating Cash Flow matches Net Profit. For {ticker}, cash conversion stands at {cash_conv:.2f}x.",
            "severity": "low" if cash_conv >= 0.8 else "high"
        },
        {
            "id": "rule_2",
            "title": "Monitor Sloan Accruals Threshold",
            "description": f"Ensure non-cash accruals ratio stays strictly under 0.05. Current metric: {accruals:.4f}.",
            "severity": "low" if abs(accruals) < 0.05 else "medium"
        },
        {
            "id": "rule_3",
            "title": "Audit Debt Coverage & Capital Expenditure",
            "description": f"Validate that capital deployment (${fcf/1e9:.2f}B FCF) is organic rather than debt-funded.",
            "severity": "low" if debt_eq < 1.5 else "medium"
        }
    ]

    final_memo = (
        f"EXECUTIVE AUDIT DOSSIER FOR {company.upper()} ({ticker})\n"
        f"Target Investment Horizon: {horizon}\n"
        f"Audit Verification Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        f"Summary: Financial statements were cross-verified via Python code sandbox execution against SEC XBRL filings. "
        f"Balance sheet balance check result: {'PASSED' if bs_balanced else 'FAILED'} (Discrepancy: ${ratios.get('bs_discrepancy', 0):,.2f}). "
        f"Sloan Accruals ratio is {accruals:.4f}, indicating {'low non-cash accounting distortion' if abs(accruals)<0.05 else 'moderate non-cash accruals'}. "
        f"Total Free Cash Flow generated: ${fcf/1e9:.2f} Billion."
    )

    logs.append({
        "step": "Synthesizer",
        "message": "Dossier synthesis complete. Ready for presentation.",
        "timestamp": datetime.datetime.now().isoformat()
    })

    return {
        **state,
        "health_scorecard": health_scorecard,
        "reality_checks": reality_checks,
        "risk_rules": risk_rules,
        "final_memo": final_memo,
        "execution_logs": logs
    }
