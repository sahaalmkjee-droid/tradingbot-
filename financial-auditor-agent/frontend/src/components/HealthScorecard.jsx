import React from 'react';
import { DollarSign, Activity, Wallet, ShieldAlert, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

export default function HealthScorecard({ scorecard, companyName, ticker }) {
  if (!scorecard || scorecard.length === 0) return null;

  const getStatusBadge = (status) => {
    switch (status) {
      case 'green':
        return {
          bg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
          icon: <CheckCircle className="w-4 h-4 text-emerald-600" />,
          label: 'Healthy'
        };
      case 'yellow':
        return {
          bg: 'bg-amber-50 text-amber-800 border-amber-200',
          icon: <AlertTriangle className="w-4 h-4 text-amber-600" />,
          label: 'Caution'
        };
      case 'red':
        return {
          bg: 'bg-red-50 text-red-800 border-red-200',
          icon: <XCircle className="w-4 h-4 text-red-600" />,
          label: 'Red Flag'
        };
      default:
        return {
          bg: 'bg-slate-50 text-slate-700 border-slate-200',
          icon: <Activity className="w-4 h-4 text-slate-500" />,
          label: 'Neutral'
        };
    }
  };

  const getCardIcon = (index) => {
    const icons = [
      <DollarSign className="w-5 h-5 text-teal-600" />,
      <Activity className="w-5 h-5 text-indigo-600" />,
      <Wallet className="w-5 h-5 text-blue-600" />,
      <ShieldAlert className="w-5 h-5 text-purple-600" />
    ];
    return icons[index % icons.length];
  };

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <span>Financial Health Scorecard</span>
          <span className="text-xs font-semibold px-2.5 py-0.5 bg-slate-100 text-slate-700 rounded-md border border-slate-200">
            {companyName} ({ticker})
          </span>
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {scorecard.map((item, idx) => {
          const badge = getStatusBadge(item.status);
          return (
            <div
              key={item.id || idx}
              className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                    {getCardIcon(idx)}
                  </div>
                  <span className={`inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-bold border ${badge.bg}`}>
                    {badge.icon}
                    <span>{badge.label}</span>
                  </span>
                </div>

                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                  {item.title}
                </h3>

                <p className="text-lg font-bold text-slate-900 tracking-tight mb-2">
                  {item.value}
                </p>
              </div>

              <p className="text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-2.5 mt-2">
                {item.detail}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
