import json
import uuid
import asyncio
import logging
from typing import Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from app.config import HOST, BACKEND_PORT
from app.schemas.audit import AuditRequest, AuditResponse
from app.agents.graph import run_audit_workflow, stream_audit_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(
    title="Autonomous Quantitative Earnings & SEC Filings Auditor API",
    version="1.0.0"
)

# CORS setup for Vite frontend (http://localhost:5174)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for task requests
TASKS_STORE: Dict[str, dict] = {}

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Autonomous Quantitative Earnings & SEC Filings Auditor",
        "port": BACKEND_PORT
    }

@app.post("/api/audit")
def start_audit(req: AuditRequest):
    task_id = str(uuid.uuid4())
    TASKS_STORE[task_id] = {
        "ticker": req.ticker.upper(),
        "horizon": req.horizon,
        "concern": req.concern,
        "status": "pending"
    }
    return {
        "task_id": task_id,
        "ticker": req.ticker.upper(),
        "status": "initiated"
    }

@app.get("/api/audit/{task_id}/stream")
async def stream_audit(task_id: str):
    if task_id not in TASKS_STORE:
        # If task_id not found, create a temporary task with ticker from query or fallback
        task_info = {"ticker": "AAPL", "horizon": "3-5 years", "concern": "General"}
    else:
        task_info = TASKS_STORE[task_id]

    ticker = task_info["ticker"]
    horizon = task_info["horizon"]
    concern = task_info["concern"]

    async def event_generator():
        # Yield initial connection message
        yield {
            "event": "message",
            "data": json.dumps({
                "type": "init",
                "task_id": task_id,
                "message": f"Initializing Multi-Agent Audit Pipeline for {ticker}..."
            })
        }
        await asyncio.sleep(0.2)

        # Stream LangGraph execution
        loop = asyncio.get_running_loop()
        
        def run_streaming():
            return list(stream_audit_workflow(ticker, horizon, concern, task_id))

        events = await loop.run_in_executor(None, run_streaming)

        for evt in events:
            yield {
                "event": "message",
                "data": json.dumps(evt)
            }
            await asyncio.sleep(0.3)

        # Run complete final state synthesis
        def run_final():
            return run_audit_workflow(ticker, horizon, concern, task_id)

        final_state = await loop.run_in_executor(None, run_final)

        yield {
            "event": "complete",
            "data": json.dumps({
                "type": "complete",
                "result": {
                    "task_id": task_id,
                    "ticker": ticker,
                    "company_name": final_state.get("company_name", ticker),
                    "horizon": horizon,
                    "concern": concern,
                    "verified_ratios": final_state.get("verified_ratios", {}),
                    "health_scorecard": final_state.get("health_scorecard", []),
                    "reality_checks": final_state.get("reality_checks", []),
                    "risk_rules": final_state.get("risk_rules", []),
                    "final_memo": final_state.get("final_memo", ""),
                    "execution_logs": final_state.get("execution_logs", [])
                }
            })
        }

    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=BACKEND_PORT, reload=True)
