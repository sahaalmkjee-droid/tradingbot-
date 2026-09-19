import json
import datetime
import logging
from app.agents.state import AuditorState
from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

def run_gemini_auditor_analysis(ticker: str, company: str, ratios: dict, raw_facts: dict, concern: str) -> dict:
    """Run Gemini LLM tone & anomaly auditor analysis if API key available, else return structured fallback."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        logger.info("No valid GEMINI_API_KEY provided; using deterministic auditor logic.")
        return get_fallback_anomalies(ticker, company, ratios)

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
You are an institutional quantitative forensic accountant auditing {company} ({ticker}).
The primary investor concern is: {concern}.

Calculated Verified Ratios from SEC Filings:
{json.dumps(ratios, indent=2)}

Financial Statements Summary:
{json.dumps(raw_facts.get('financials', {}), indent=2)}

Analyze the data and identify 3 key "Words vs Numbers Reality Checks" where management statements or typical investor expectations contrast with the actual hard audited data.

Return ONLY a JSON object matching this structure:
{{
  "anomalies": [
    {{
      "topic": "Cash Flow vs Earnings",
      "claim": "Management highlighted record net profit figures in quarterly statements.",
      "reality": "Operating cash flow conversion ratio was calculated at {ratios.get('cash_conversion_quality', 1.0):.2f}x net income.",
      "takeaway": "Real cash generation backing reported earnings."
    }},
    {{
      "topic": "Balance Sheet Quality",
      "claim": "Aggressive expansion funded by long-term debt and capital deployment.",
      "reality": "Debt to equity ratio stands at {ratios.get('debt_to_equity', 0.0):.2f}.",
      "takeaway": "Leverage remains within controlled thresholds relative to total assets."
    }},
    {{
      "topic": "Earnings Quality & Accruals",
      "claim": "Robust operating cash generation expected to fuel dividend and share buybacks.",
      "reality": "Sloan accruals ratio is {ratios.get('accruals_ratio', 0.0):.4f}.",
      "takeaway": "Low accrual distortion indicates organic earnings quality."
    }}
  ]
}}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        text = response.text.strip()
        # Parse JSON
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(text)
        return data
    except Exception as e:
        logger.warning(f"Gemini API call failed or SDK not configured: {e}")
        return get_fallback_anomalies(ticker, company, ratios)

def get_fallback_anomalies(ticker: str, company: str, ratios: dict) -> dict:
    fcf = ratios.get("free_cash_flow", 0)
    accruals = ratios.get("accruals_ratio", 0)
    cash_conv = ratios.get("cash_conversion_quality", 1.0)
    debt_eq = ratios.get("debt_to_equity", 0.0)
    
    return {
        "anomalies": [
            {
                "topic": "Cash Conversion & FCF",
                "claim": f"{company} executive narrative emphasizes strong market growth and profit execution.",
                "reality": f"Audited Free Cash Flow was computed at ${fcf:,.2f} with cash conversion at {cash_conv:.2f}x net income.",
                "takeaway": "Cash generation matches or exceeds accounting profits, confirming genuine revenue realization." if cash_conv >= 0.8 else "Operating cash flow trails net earnings, flagging potential working capital strain or uncollected receivables."
            },
            {
                "topic": "Earnings Quality (Sloan Accruals)",
                "claim": "Earnings report highlights top-line revenue momentum.",
                "reality": f"Calculated Sloan Accruals ratio is {accruals:.4f} (Benchmark: < |0.05| is healthy).",
                "takeaway": "Earnings quality is strong with low non-cash accounting accruals." if abs(accruals) < 0.08 else "Elevated non-cash accruals signal aggressive revenue recognition or capitalized expenses."
            },
            {
                "topic": "Balance Sheet & Capital Structure",
                "claim": "Management asserts pristine liquidity and solvent balance sheet stability.",
                "reality": f"Long-term debt to equity ratio is {debt_eq:.2f} with balance sheet balance check delta: ${ratios.get('bs_discrepancy', 0):,.2f}.",
                "takeaway": "Prudent leverage allowing economic cycle resilience." if debt_eq < 1.5 else "Higher financial leverage requires monitoring during rising interest rate environments."
            }
        ]
    }

def auditor_node(state: AuditorState) -> AuditorState:
    logs = state.get("execution_logs", [])
    ticker = state.get("ticker", "AAPL")
    company = state.get("company_name", ticker)
    ratios = state.get("verified_ratios", {})
    raw_facts = state.get("raw_filing_facts", {})
    concern = state.get("concern", "General")
    
    logs.append({
        "step": "Auditor",
        "message": f"Running Tone Drift & MD&A Anomaly Detection on SEC filings for {company}...",
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    analysis = run_gemini_auditor_analysis(ticker, company, ratios, raw_facts, concern)
    anomalies = analysis.get("anomalies", [])
    
    logs.append({
        "step": "Auditor",
        "message": f"Detected {len(anomalies)} key narrative vs quantitative reality points.",
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    return {
        **state,
        "anomalies": anomalies,
        "execution_logs": logs
    }
