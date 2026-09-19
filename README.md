# Autonomous Quantitative Earnings & SEC Filings Auditor

An institutional-grade multi-agent audit system that takes a public US stock ticker, fetches real SEC EDGAR facts (XBRL JSON) and market data (`yfinance`), runs deterministic mathematical checks on financial statements via Python code execution inside an isolated sandbox, performs MD&A tone drift analysis using Google Gemini, and renders an executive dossier for non-technical investors.

---

## 🏛️ System Architecture & Workflow

```
                          +-----------------------------------+
                          |    User Query (Ticker: NVDA)      |
                          +-----------------------------------+
                                            |
                                            v
                          +-----------------------------------+
                          |  Node 1: SEC XBRL Extractor       |
                          |  (EDGAR Facts JSON & yfinance)    |
                          +-----------------------------------+
                                            |
                                            v
                          +-----------------------------------+
                          |  Node 2: Code Interpreter Sandbox |
                          |  (Deterministic Python Execution)  |
                          +-----------------------------------+
                                            |
                                            v
                          +-----------------------------------+
                          |  Node 3: MD&A Tone Drift Auditor  |
                          |  (Google Gemini 2.5/1.5 API)      |
                          +-----------------------------------+
                                            |
                                            v
                          +-----------------------------------+
                          |  Node 4: Dossier Synthesizer      |
                          |  (Health Scorecard & Reality Matrix)|
                          +-----------------------------------+
                                            |
                                            v
                          +-----------------------------------+
                          | React Dashboard (Port :5174)      |
                          +-----------------------------------+
```

---

## ✨ Key Features

- **SEC EDGAR XBRL Data Ingestion**: Direct retrieval of primary financial facts (Balance Sheet, Income Statement, Cash Flow) from `data.sec.gov` with compliant `User-Agent` headers and automated `yfinance` fallback.
- **Deterministic Python Execution Sandbox**: Executes verification calculations in an isolated Python subprocess with a strict 5-second timeout:
  - Balance Sheet Balance Check ($Assets = Liabilities + Equity$)
  - Sloan Accruals Ratio ($(Net Income - Operating Cash Flow) / Total Assets$)
  - Free Cash Flow ($FCF = Operating Cash Flow - CapEx$)
  - Debt-to-Equity & Cash Conversion Quality
- **Tone Drift & MD&A Anomaly Auditor**: Leverages Google Gemini to cross-reference executive narrative against audited quantitative facts.
- **Institutional Off-White Dashboard**:
  - **Live LangGraph Agent Execution Terminal**: Real-time Server-Sent Events (SSE) streaming.
  - **Financial Health Scorecard**: 4 visual status cards with Emerald/Amber/Crimson risk badges.
  - **Words vs. Numbers Reality Check Matrix**: Comparative table contrasting management narrative vs audited numbers vs plain-English takeaways.
  - **3 Golden Rules Before Buying**: Actionable warning checklist for retail investors.

---

## 🌐 Port Allocation Policy

To prevent localhost collisions:
- **FastAPI Backend**: `8088` (`http://localhost:8088`)
- **React Frontend (Vite)**: `5174` (`http://localhost:5174`)

---

## 📁 Directory Structure

```
financial-auditor-agent/
├── .env.example
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── state.py
│   │   │   ├── graph.py
│   │   │   ├── extractor.py
│   │   │   ├── interpreter.py
│   │   │   ├── auditor.py
│   │   │   └── synthesizer.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── edgar.py
│   │   │   ├── market.py
│   │   │   └── sandbox.py
│   │   └── schemas/
│   │       └── audit.py
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── components/
        │   ├── Header.jsx
        │   ├── SearchBar.jsx
        │   ├── AgentTerminalStream.jsx
        │   ├── HealthScorecard.jsx
        │   ├── RealityCheckMatrix.jsx
        │   └── RiskReport.jsx
        └── services/
            └── api.js
```

---

## 🚀 Quickstart Guide

### 1. Environment Configuration

Create a `.env` file in `financial-auditor-agent/`:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
BACKEND_PORT=8088
FRONTEND_PORT=5174
```

### 2. Backend Setup (FastAPI & LangGraph)

```bash
cd financial-auditor-agent/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8088 --reload
```

### 3. Frontend Setup (React & Vite)

```bash
cd financial-auditor-agent/frontend
npm install
npm run dev -- --port 5174
```

### 4. Access the Auditor

Open **[http://localhost:5174](http://localhost:5174)** in your web browser.

---

## 🔐 Security & Compliance

- **SEC EDGAR Guidelines**: Declares a compliant `User-Agent` header (`User-Agent: FinancialAuditorBot admin@auditplatform.local`).
- **Sandbox Isolation**: Code execution runs inside a restricted subprocess bounded by execution timeouts.
- **Environment Protection**: `.env` files containing API credentials are explicitly ignored in `.gitignore`.

---

## 📜 License

MIT License. Built for institutional-grade quantitative audit and educational research.
