import json
import datetime
import logging
from app.agents.state import AuditorState
from app.tools.sandbox import execute_python_code

logger = logging.getLogger(__name__)

def generate_verification_script(financials: dict) -> str:
    """Generate a self-contained Python script to deterministically verify balance sheet and accounting ratios."""
    fin_json = json.dumps(financials)
    return f"""import json

fin = {fin_json}

assets = float(fin.get("Assets", 0))
liabilities = float(fin.get("Liabilities", 0))
equity = float(fin.get("StockholdersEquity", 0))
cash = float(fin.get("CashAndEquivalents", 0))
inventory = float(fin.get("Inventory", 0))
receivables = float(fin.get("AccountsReceivable", 0))
lt_debt = float(fin.get("LongTermDebt", 0))

revenue = float(fin.get("Revenue", 0))
gross_profit = float(fin.get("GrossProfit", 0))
operating_income = float(fin.get("OperatingIncome", 0))
net_income = float(fin.get("NetIncome", 0))
ocf = float(fin.get("OperatingCashFlow", 0))
capex = float(fin.get("CapEx", 0))

# 1. Balance Sheet Balance Verification
expected_assets = liabilities + equity
bs_discrepancy = round(assets - expected_assets, 2)
bs_balanced = abs(bs_discrepancy) < 0.05 * assets if assets else True

# 2. Free Cash Flow
fcf = ocf - capex

# 3. Accruals Ratio (Sloan Ratio): (Net Income - Operating Cash Flow) / Total Assets
accruals_ratio = round((net_income - ocf) / assets, 4) if assets > 0 else 0.0

# 4. Debt to Equity & Debt to Assets
debt_to_equity = round(lt_debt / equity, 4) if equity > 0 else 0.0
debt_to_assets = round(lt_debt / assets, 4) if assets > 0 else 0.0

# 5. Margins & Cash Conversion Ratio
gross_margin = round(gross_profit / revenue, 4) if revenue > 0 else 0.0
operating_margin = round(operating_income / revenue, 4) if revenue > 0 else 0.0
net_margin = round(net_income / revenue, 4) if revenue > 0 else 0.0
cash_conversion_quality = round(ocf / net_income, 4) if net_income > 0 else 0.0

result = {{
    "bs_balanced": bs_balanced,
    "bs_discrepancy": bs_discrepancy,
    "assets": assets,
    "liabilities": liabilities,
    "equity": equity,
    "cash": cash,
    "lt_debt": lt_debt,
    "revenue": revenue,
    "gross_profit": gross_profit,
    "net_income": net_income,
    "operating_cash_flow": ocf,
    "capex": capex,
    "free_cash_flow": fcf,
    "accruals_ratio": accruals_ratio,
    "debt_to_equity": debt_to_equity,
    "gross_margin": gross_margin,
    "net_margin": net_margin,
    "cash_conversion_quality": cash_conversion_quality
}}

print(json.dumps(result))
"""

def interpreter_node(state: AuditorState) -> AuditorState:
    logs = state.get("execution_logs", [])
    raw_facts = state.get("raw_filing_facts", {})
    financials = raw_facts.get("financials", {})
    
    logs.append({
        "step": "Interpreter",
        "message": "Generating Python verification script for balance sheet equation, FCF, and Sloan Accruals ratio...",
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    code = generate_verification_script(financials)
    
    # Run in sandbox
    res = execute_python_code(code, timeout=5)
    
    logs.append({
        "step": "Interpreter",
        "message": f"Sandbox code execution completed (Exit code: {res['returncode']})",
        "timestamp": datetime.datetime.now().isoformat(),
        "details": res['stdout'] if res['success'] else res['stderr']
    })
    
    verified_ratios = {}
    if res['success'] and res['parsed_result']:
        verified_ratios = res['parsed_result']
    else:
        # Fallback inline calculation if subprocess execution fails
        assets = float(financials.get("Assets", 1))
        liabilities = float(financials.get("Liabilities", 0))
        equity = float(financials.get("StockholdersEquity", 1))
        net_inc = float(financials.get("NetIncome", 0))
        ocf = float(financials.get("OperatingCashFlow", 0))
        capex = float(financials.get("CapEx", 0))
        lt_debt = float(financials.get("LongTermDebt", 0))
        
        verified_ratios = {
            "bs_balanced": abs(assets - (liabilities + equity)) < 0.05 * assets,
            "bs_discrepancy": round(assets - (liabilities + equity), 2),
            "free_cash_flow": ocf - capex,
            "accruals_ratio": round((net_inc - ocf) / assets, 4) if assets else 0,
            "debt_to_equity": round(lt_debt / equity, 4) if equity else 0,
            "cash_conversion_quality": round(ocf / net_inc, 4) if net_inc else 0,
            "net_margin": round(net_inc / float(financials.get("Revenue", 1)), 4)
        }
        
    return {
        **state,
        "code_to_run": code,
        "verified_ratios": verified_ratios,
        "execution_logs": logs
    }
