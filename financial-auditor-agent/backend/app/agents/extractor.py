import datetime
import logging
from app.agents.state import AuditorState
from app.tools.edgar import fetch_sec_xbrl_facts

logger = logging.getLogger(__name__)

def extractor_node(state: AuditorState) -> AuditorState:
    ticker = state.get("ticker", "AAPL").upper()
    logs = state.get("execution_logs", [])
    
    log_entry = {
        "step": "Extractor",
        "message": f"Fetching SEC EDGAR XBRL filings and market financial statements for ticker: {ticker}",
        "timestamp": datetime.datetime.now().isoformat()
    }
    logs.append(log_entry)
    
    facts_data = fetch_sec_xbrl_facts(ticker)
    
    source = facts_data.get("source", "SEC EDGAR")
    company_name = facts_data.get("company_name", ticker)
    
    logs.append({
        "step": "Extractor",
        "message": f"Successfully retrieved primary facts via {source} for {company_name}",
        "timestamp": datetime.datetime.now().isoformat(),
        "details": f"Assets: ${facts_data.get('financials', {}).get('Assets', 0):,.2f}, Revenue: ${facts_data.get('financials', {}).get('Revenue', 0):,.2f}"
    })
    
    return {
        **state,
        "raw_filing_facts": facts_data,
        "company_name": company_name,
        "execution_logs": logs
    }
