import React, { useState } from 'react';
import { Search, Loader2, Sparkles, TrendingUp } from 'lucide-react';

export default function SearchBar({ onAudit, isLoading }) {
  const [ticker, setTicker] = useState('NVDA');
  const [horizon, setHorizon] = useState('3-5 years');
  const [concern, setConcern] = useState('General');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker.trim() && !isLoading) {
      onAudit(ticker.toUpperCase().trim(), horizon, concern);
    }
  };

  const presetTickers = ['NVDA', 'AAPL', 'MSFT', 'TSLA', 'AMZN', 'META'];

  return (
    <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs mb-6">
      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
        
        {/* Ticker Input */}
        <div className="md:col-span-4">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
            US Stock Ticker Symbol
          </label>
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              placeholder="e.g. AAPL, NVDA, TSLA"
              className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-semibold uppercase placeholder:normal-case placeholder:font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all text-sm"
              required
            />
          </div>
        </div>

        {/* Investment Horizon */}
        <div className="md:col-span-3">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
            Investment Horizon
          </label>
          <select
            value={horizon}
            onChange={(e) => setHorizon(e.target.value)}
            className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all"
          >
            <option value="1 year">1 Year (Short-term)</option>
            <option value="3-5 years">3-5 Years (Medium-term)</option>
            <option value="10+ years">10+ Years (Long-term Buy & Hold)</option>
          </select>
        </div>

        {/* Primary Concern */}
        <div className="md:col-span-3">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
            Audit Focus / Concern
          </label>
          <select
            value={concern}
            onChange={(e) => setConcern(e.target.value)}
            className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all"
          >
            <option value="General">General Financial Audit</option>
            <option value="Earnings Quality">Earnings Quality & Accruals</option>
            <option value="Debt & Liquidity">Debt Solvency & Free Cash Flow</option>
            <option value="Working Capital">Inventory Pile-up & Receivables</option>
          </select>
        </div>

        {/* Submit Button */}
        <div className="md:col-span-2">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 px-4 bg-teal-600 hover:bg-teal-700 active:bg-teal-800 disabled:bg-slate-300 text-white font-semibold text-sm rounded-lg shadow-xs flex items-center justify-center space-x-2 transition-all cursor-pointer"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Auditing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Audit Ticker</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Preset Ticker Chips */}
      <div className="mt-3.5 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-400 font-medium flex items-center gap-1">
          <TrendingUp className="w-3.5 h-3.5" /> Quick Audit:
        </span>
        {presetTickers.map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => {
              setTicker(t);
              if (!isLoading) onAudit(t, horizon, concern);
            }}
            className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-md transition-all cursor-pointer"
          >
            {t}
          </button>
        ))}
      </div>
    </div>
  );
}
