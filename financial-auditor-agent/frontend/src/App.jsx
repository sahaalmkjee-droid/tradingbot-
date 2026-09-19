import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import AgentTerminalStream from './components/AgentTerminalStream';
import HealthScorecard from './components/HealthScorecard';
import RealityCheckMatrix from './components/RealityCheckMatrix';
import RiskReport from './components/RiskReport';
import { startAuditJob, connectAuditStream } from './services/api';
import { ShieldAlert, RefreshCw } from 'lucide-react';

export default function App() {
  const [ticker, setTicker] = useState('NVDA');
  const [horizon, setHorizon] = useState('3-5 years');
  const [concern, setConcern] = useState('General');
  const [isLoading, setIsLoading] = useState(false);
  const [isLiveStream, setIsLiveStream] = useState(false);
  const [activeNode, setActiveNode] = useState('');
  const [logs, setLogs] = useState([]);
  const [auditResult, setAuditResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRunAudit = async (selectedTicker, selectedHorizon, selectedConcern) => {
    setIsLoading(true);
    setIsLiveStream(true);
    setError(null);
    setLogs([]);
    setAuditResult(null);
    setTicker(selectedTicker);
    setHorizon(selectedHorizon);
    setConcern(selectedConcern);

    try {
      // 1. Initiate job on backend port 8088
      const job = await startAuditJob(selectedTicker, selectedHorizon, selectedConcern);
      const taskId = job.task_id;

      // 2. Connect to SSE stream
      connectAuditStream(
        taskId,
        (stepData) => {
          if (stepData.log) {
            setLogs((prev) => [...prev, stepData.log]);
            setActiveNode(stepData.node || stepData.log.step);
          }
        },
        (resultData) => {
          setAuditResult(resultData);
          setIsLoading(false);
          setIsLiveStream(false);
          setActiveNode('COMPLETE');
        },
        (err) => {
          console.error("Stream connection error", err);
          setError("Failed to stream audit updates from backend server on port 8088.");
          setIsLoading(false);
          setIsLiveStream(false);
        }
      );
    } catch (e) {
      console.error("Failed to start audit job", e);
      setError(e.message || "Failed to connect to backend on http://localhost:8088");
      setIsLoading(false);
      setIsLiveStream(false);
    }
  };

  // Run initial audit on load
  useEffect(() => {
    handleRunAudit('NVDA', '3-5 years', 'General');
  }, []);

  return (
    <div className="min-h-screen bg-[#F8F9FA] text-slate-900 flex flex-col font-sans">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6">
        <SearchBar onAudit={handleRunAudit} isLoading={isLoading} />

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-800 text-sm flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5 text-red-600 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => handleRunAudit(ticker, horizon, concern)}
              className="px-3 py-1 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 text-xs flex items-center gap-1 cursor-pointer"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Retry
            </button>
          </div>
        )}

        {/* Live Execution Stream */}
        <AgentTerminalStream
          logs={logs}
          isLive={isLiveStream}
          activeNode={activeNode}
        />

        {/* Audit Results Dashboard */}
        {auditResult && (
          <div className="animate-in fade-in duration-500">
            <HealthScorecard
              scorecard={auditResult.health_scorecard}
              companyName={auditResult.company_name}
              ticker={auditResult.ticker}
            />

            <RealityCheckMatrix
              realityChecks={auditResult.reality_checks}
            />

            <RiskReport
              riskRules={auditResult.risk_rules}
              finalMemo={auditResult.final_memo}
              verifiedRatios={auditResult.verified_ratios}
            />
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        Autonomous Quantitative Earnings & SEC Filings Auditor • Multi-Agent Institutional Audit Engine
      </footer>
    </div>
  );
}
