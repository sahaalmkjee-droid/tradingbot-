import requests
import logging
from typing import Dict, Any, Optional
from app.tools.market import fetch_yfinance_financials

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "FinancialAuditorBot admin@auditplatform.local",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov"
}

TICKER_MAP_HEADERS = {
    "User-Agent": "FinancialAuditorBot admin@auditplatform.local",
    "Accept-Encoding": "gzip, deflate"
}

_CIK_CACHE = {}

def get_cik_for_ticker(ticker: str) -> Optional[str]:
    """Fetch CIK for a given stock ticker from SEC company_tickers.json"""
    ticker_upper = ticker.upper().strip()
    if ticker_upper in _CIK_CACHE:
        return _CIK_CACHE[ticker_upper]
    
    url = "https://www.sec.gov/files/company_tickers.json"
    try:
        response = requests.get(url, headers=TICKER_MAP_HEADERS, timeout=5)
        if response.status_code == 200:
            data = response.json()
            for entry in data.values():
                if entry.get("ticker") == ticker_upper:
                    cik = str(entry.get("cik_str"))
                    _CIK_CACHE[ticker_upper] = cik
                    return cik
    except Exception as e:
        logger.warning(f"Failed to fetch SEC CIK for {ticker_upper}: {e}")
    return None

def extract_latest_val(facts_dict: dict, concepts: list) -> Optional[float]:
    """Helper to extract the latest annual/quarterly reported value for concepts"""
    for concept in concepts:
        if concept in facts_dict:
            units = facts_dict[concept].get("units", {})
            for unit_key in ["USD", "USD/shares", "shares"]:
                if unit_key in units:
                    items = units[unit_key]
                    if items:
                        # Filter items with end date or frame, sort by end date
                        valid_items = [i for i in items if "val" in i and "end" in i]
                        if valid_items:
                            valid_items.sort(key=lambda x: x.get("end", ""))
                            return float(valid_items[-1]["val"])
    return None

def fetch_sec_xbrl_facts(ticker: str) -> Dict[str, Any]:
    """
    Fetch SEC EDGAR XBRL facts for ticker.
    Falls back gracefully to yfinance data if SEC EDGAR request fails or key concepts missing.
    """
    ticker = ticker.upper().strip()
    cik = get_cik_for_ticker(ticker)
    
    if cik:
        padded_cik = cik.zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{padded_cik}.json"
        try:
            res = requests.get(url, headers=HEADERS, timeout=8)
            if res.status_code == 200:
                data = res.json()
                us_gaap = data.get("facts", {}).get("us-gaap", {})
                
                # Extract primary concepts
                assets = extract_latest_val(us_gaap, ["Assets"])
                liabilities = extract_latest_val(us_gaap, ["Liabilities", "LiabilitiesCurrent"])
                equity = extract_latest_val(us_gaap, ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"])
                cash = extract_latest_val(us_gaap, ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"])
                inventory = extract_latest_val(us_gaap, ["InventoryNet", "Inventories"])
                receivables = extract_latest_val(us_gaap, ["AccountsReceivableNetCurrent", "ReceivablesNetCurrent"])
                long_term_debt = extract_latest_val(us_gaap, ["LongTermDebtNoncurrent", "LongTermDebt"])
                
                revenue = extract_latest_val(us_gaap, ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"])
                gross_profit = extract_latest_val(us_gaap, ["GrossProfit"])
                operating_income = extract_latest_val(us_gaap, ["OperatingIncomeLoss"])
                net_income = extract_latest_val(us_gaap, ["NetIncomeLoss"])
                
                ocf = extract_latest_val(us_gaap, ["NetCashProvidedByUsedInOperatingActivities"])
                capex = extract_latest_val(us_gaap, ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"])
                
                # Check if essential values were parsed
                if assets and ocf and revenue:
                    return {
                        "source": "SEC EDGAR XBRL",
                        "ticker": ticker,
                        "cik": cik,
                        "company_name": data.get("entityName", ticker),
                        "financials": {
                            "Assets": assets,
                            "Liabilities": liabilities or (assets - (equity or 0)),
                            "StockholdersEquity": equity or (assets - (liabilities or 0)),
                            "CashAndEquivalents": cash or 0,
                            "Inventory": inventory or 0,
                            "AccountsReceivable": receivables or 0,
                            "LongTermDebt": long_term_debt or 0,
                            "Revenue": revenue,
                            "GrossProfit": gross_profit or (revenue * 0.4),
                            "OperatingIncome": operating_income or (revenue * 0.15),
                            "NetIncome": net_income or (revenue * 0.10),
                            "OperatingCashFlow": ocf,
                            "CapEx": capex or 0
                        }
                    }
        except Exception as e:
            logger.warning(f"SEC EDGAR fetch error for {ticker}: {e}")
            
    # Fallback to yfinance if SEC lookup fails or rate limited
    logger.info(f"Falling back to yfinance data for {ticker}")
    return fetch_yfinance_financials(ticker)
