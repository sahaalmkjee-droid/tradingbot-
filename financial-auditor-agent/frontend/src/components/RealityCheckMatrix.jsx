import React from 'react';
import { Scale, Quote, BarChart2, Lightbulb } from 'lucide-react';

export default function RealityCheckMatrix({ realityChecks }) {
  if (!realityChecks || realityChecks.length === 0) return null;

  return (
    <div className="bg-white border border-slate-200/90 rounded-xl p-6 shadow-xs mb-8">
      <div className="flex items-center space-x-2.5 mb-5 pb-3 border-b border-slate-100">
        <div className="p-2 bg-amber-50 text-amber-700 rounded-lg border border-amber-200">
          <Scale className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-slate-900 tracking-tight">
            Words vs. Numbers Reality Check Matrix
          </h2>
          <p className="text-xs text-slate-500">
            Cross-referencing executive press releases & MD&A narratives against audited SEC XBRL metrics.
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/80 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-600">
              <th className="py-3 px-4 w-1/4">Topic & Management Narrative</th>
              <th className="py-3 px-4 w-1/3">Audited SEC XBRL Data</th>
              <th className="py-3 px-4 w-5/12">Plain-English Investor Takeaway</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-xs">
            {realityChecks.map((item, idx) => (
              <tr key={item.id || idx} className="hover:bg-slate-50/50 transition-colors">
                
                {/* Claim */}
                <td className="py-4 px-4 align-top">
                  <div className="font-semibold text-slate-900 mb-1 flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                    {item.topic}
                  </div>
                  <div className="italic text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-200/60 mt-1.5">
                    <Quote className="w-3 h-3 text-slate-400 inline mr-1" />
                    "{item.claim}"
                  </div>
                </td>

                {/* Reality */}
                <td className="py-4 px-4 align-top">
                  <div className="font-mono text-slate-800 bg-teal-50/60 p-2.5 rounded-lg border border-teal-200/60 font-medium">
                    <BarChart2 className="w-3.5 h-3.5 text-teal-600 inline mr-1.5" />
                    {item.reality}
                  </div>
                </td>

                {/* Takeaway */}
                <td className="py-4 px-4 align-top">
                  <div className="text-slate-700 bg-slate-50 p-2.5 rounded-lg border border-slate-200/60 leading-relaxed font-medium">
                    <Lightbulb className="w-3.5 h-3.5 text-amber-500 inline mr-1.5" />
                    {item.takeaway}
                  </div>
                </td>

              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
