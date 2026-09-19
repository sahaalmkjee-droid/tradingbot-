import React from 'react';
import { ShieldCheck, Cpu, Database } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200/90 shadow-xs px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-slate-900 text-teal-400 rounded-lg shadow-sm">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              Autonomous Quantitative Earnings & SEC Filings Auditor
            </h1>
            <p className="text-xs text-slate-500 font-medium flex items-center gap-2 mt-0.5">
              <span>Multi-Agent LangGraph Pipeline</span>
              <span className="text-slate-300">•</span>
              <span>SEC EDGAR XBRL Facts</span>
              <span className="text-slate-300">•</span>
              <span>Python Code Sandbox Verification</span>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse mr-1.5"></span>
            Backend :8088
          </span>
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            Frontend :5174
          </span>
        </div>
      </div>
    </header>
  );
}
