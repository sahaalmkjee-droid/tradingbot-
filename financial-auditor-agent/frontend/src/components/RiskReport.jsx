import React from 'react';
import { ShieldCheck, AlertCircle, FileText, CheckSquare, ExternalLink } from 'lucide-react';

export default function RiskReport({ riskRules, finalMemo, verifiedRatios }) {
  if (!riskRules && !finalMemo) return null;

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      default:
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
      
      {/* 3 Golden Rules Checklist */}
      <div className="lg:col-span-7 bg-white border border-slate-200/90 rounded-xl p-6 shadow-xs">
        <div className="flex items-center space-x-2.5 mb-4 pb-3 border-b border-slate-100">
          <div className="p-2 bg-teal-50 text-teal-700 rounded-lg border border-teal-200">
            <CheckSquare className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">
              3 Actionable Rules Before Buying
            </h2>
            <p className="text-xs text-slate-500">
              Essential quantitative sanity checks for retail and institutional investors.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {riskRules && riskRules.map((rule, idx) => (
            <div
              key={rule.id || idx}
              className="p-4 bg-slate-50/80 border border-slate-200/80 rounded-lg flex items-start space-x-3 hover:border-slate-300 transition-colors"
            >
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-slate-900 text-teal-400 font-mono text-xs font-bold flex items-center justify-center mt-0.5">
                {idx + 1}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <h3 className="text-xs font-bold text-slate-900">
                    {rule.title}
                  </h3>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getSeverityBadge(rule.severity)}`}>
                    {rule.severity} Priority
                  </span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {rule.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Executive Memo Card */}
      <div className="lg:col-span-5 bg-white border border-slate-200/90 rounded-xl p-6 shadow-xs flex flex-col justify-between">
        <div>
          <div className="flex items-center space-x-2.5 mb-4 pb-3 border-b border-slate-100">
            <div className="p-2 bg-indigo-50 text-indigo-700 rounded-lg border border-indigo-200">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900 tracking-tight">
                Executive Audit Memo
              </h2>
              <p className="text-xs text-slate-500">
                Automated quantitative synthesis output.
              </p>
            </div>
          </div>

          <div className="bg-slate-950 text-slate-200 font-mono text-xs p-4 rounded-lg border border-slate-800 leading-relaxed whitespace-pre-wrap max-h-80 overflow-y-auto custom-scrollbar">
            {finalMemo || "No memo generated yet."}
          </div>
        </div>

        {verifiedRatios && (
          <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-[11px] font-mono">
            <div className="bg-slate-50 p-2 rounded border border-slate-200">
              <span className="text-slate-500 block">Accruals Ratio:</span>
              <span className="font-bold text-slate-900">{verifiedRatios.accruals_ratio ?? 'N/A'}</span>
            </div>
            <div className="bg-slate-50 p-2 rounded border border-slate-200">
              <span className="text-slate-500 block">Debt/Equity:</span>
              <span className="font-bold text-slate-900">{verifiedRatios.debt_to_equity ?? 'N/A'}</span>
            </div>
          </div>
        )}
      </div>

    </div>
  );
}
