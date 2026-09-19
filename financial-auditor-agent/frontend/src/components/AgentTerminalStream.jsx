import React, { useState } from 'react';
import { Terminal, ChevronDown, ChevronUp, CheckCircle2, Code2, Cpu, FileSpreadsheet, Bot } from 'lucide-react';

export default function AgentTerminalStream({ logs, isLive, activeNode }) {
  const [isOpen, setIsOpen] = useState(true);

  const getStepIcon = (step) => {
    switch (step) {
      case 'Extractor':
        return <FileSpreadsheet className="w-3.5 h-3.5 text-blue-400" />;
      case 'Interpreter':
        return <Code2 className="w-3.5 h-3.5 text-amber-400" />;
      case 'Auditor':
        return <Bot className="w-3.5 h-3.5 text-emerald-400" />;
      case 'Synthesizer':
        return <Cpu className="w-3.5 h-3.5 text-purple-400" />;
      default:
        return <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />;
    }
  };

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-lg mb-6 text-slate-200">
      {/* Header Pill */}
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between cursor-pointer hover:bg-slate-800/80 transition-colors"
      >
        <div className="flex items-center space-x-3">
          <Terminal className="w-4 h-4 text-teal-400" />
          <span className="text-xs font-mono font-semibold tracking-wide text-slate-200 uppercase">
            LangGraph Agent Execution Stream
          </span>
          {isLive && (
            <span className="flex items-center space-x-1.5 px-2 py-0.5 rounded-full text-[10px] font-mono bg-teal-950 text-teal-300 border border-teal-800">
              <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-ping"></span>
              <span>LIVE ACTIVE: {activeNode || 'EXECUTING'}</span>
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2 text-slate-400 text-xs font-mono">
          <span>{logs.length} step(s)</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </div>

      {/* Terminal Output */}
      {isOpen && (
        <div className="p-4 font-mono text-xs max-h-64 overflow-y-auto space-y-2 custom-scrollbar bg-slate-950">
          {logs.length === 0 ? (
            <div className="text-slate-500 italic py-2">
              Waiting for agent pipeline to initialize...
            </div>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="flex items-start space-x-2.5 py-1 border-b border-slate-900/60 last:border-0">
                <span className="text-slate-500 text-[10px] mt-0.5 min-w-[65px]">
                  {log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : '00:00:00'}
                </span>
                <span className="mt-0.5">{getStepIcon(log.step)}</span>
                <div className="flex-1">
                  <span className="font-semibold text-slate-300 mr-2">
                    [{log.step || 'Agent'}]
                  </span>
                  <span className="text-slate-100">{log.message}</span>
                  {log.details && (
                    <pre className="mt-1 p-2 bg-slate-900 rounded text-[11px] text-teal-300 overflow-x-auto border border-slate-800">
                      {log.details}
                    </pre>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
