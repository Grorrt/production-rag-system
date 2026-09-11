import { useState, useEffect } from "react";
import { getEvalResults } from "../hooks/use_rag_api";

interface EvalData { last_run: string; overall_score: number; retrieval: Record<string, number>; generation: Record<string, number>; latency: Record<string, number> }

interface DashboardProps { token: string }

function Dashboard({ token }: DashboardProps) {
  const [data, setData] = useState<EvalData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEvalResults(token).then(setData).catch(console.error).finally(() => setLoading(false));
  }, [token]);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <span className="w-8 h-8 border-[3px] border-primary-300 border-t-primary-600 rounded-full animate-spin" />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-3 text-surface-400">
        <div className="w-16 h-16 rounded-2xl bg-surface-100 dark:bg-surface-800 flex items-center justify-center">
          <ChartIcon />
        </div>
        <p className="text-sm">No evaluation data available yet</p>
        <p className="text-xs">Run an evaluation from the backend to see metrics</p>
      </div>
    );
  }

  const scoreColor = data.overall_score >= 0.8 ? "text-emerald-500" : data.overall_score >= 0.6 ? "text-amber-500" : "text-red-500";
  const scoreBg = data.overall_score >= 0.8 ? "bg-emerald-50 dark:bg-emerald-900/20" : data.overall_score >= 0.6 ? "bg-amber-50 dark:bg-amber-900/20" : "bg-red-50 dark:bg-red-900/20";

  return (
    <div className="flex-1 overflow-y-auto px-4 lg:px-8 py-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-surface-900 dark:text-surface-50">Dashboard</h2>
          <p className="text-sm text-surface-400 mt-0.5">System performance metrics</p>
        </div>
        <div className={`px-3 py-1.5 rounded-lg text-xs font-medium ${scoreBg} ${scoreColor}`}>
          Last: {new Date(data.last_run).toLocaleDateString()}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard icon={<TargetIcon />} label="Overall Score" value={`${(data.overall_score * 100).toFixed(0)}%`}
          color={scoreColor} subtitle={`${data.overall_score >= 0.8 ? "Excellent" : data.overall_score >= 0.6 ? "Good" : "Needs improvement"}`} />
        <MetricCard icon={<ClockIcon />} label="P50 Latency" value={`${(data.latency.p50_ms || 0).toFixed(0)}ms`}
          color={data.latency.p50_ms < 3000 ? "text-emerald-500" : "text-amber-500"} subtitle="Median response time" />
        <MetricCard icon={<ClockIcon />} label="P95 Latency" value={`${(data.latency.p95_ms || 0).toFixed(0)}ms`}
          color={data.latency.p95_ms < 8000 ? "text-emerald-500" : "text-amber-500"} subtitle="95th percentile" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <MetricTable title="Retrieval Metrics" icon={<SearchIcon />} data={data.retrieval} goodThreshold={0.8} />
        <MetricTable title="Generation Metrics" icon={<SparkleIcon />} data={data.generation} goodThreshold={0.8} />
      </div>
    </div>
  );
}

function MetricCard({ icon, label, value, color, subtitle }: { icon: JSX.Element; label: string; value: string; color: string; subtitle: string }) {
  return (
    <div className="glass-card p-5 transition-all duration-200 hover:shadow-xl hover:shadow-surface-900/5 dark:hover:shadow-black/20">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-9 h-9 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
          {icon}
        </div>
        <p className="text-sm font-medium text-surface-500 dark:text-surface-400">{label}</p>
      </div>
      <p className={`text-3xl font-extrabold ${color}`}>{value}</p>
      <p className="text-xs text-surface-400 mt-1">{subtitle}</p>
    </div>
  );
}

function MetricTable({ title, icon, data, goodThreshold }: { title: string; icon: JSX.Element; data: Record<string, number>; goodThreshold: number }) {
  return (
    <div className="glass-card p-5">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-7 h-7 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
          {icon}
        </div>
        <h3 className="text-sm font-semibold text-surface-900 dark:text-surface-50">{title}</h3>
      </div>
      <div className="space-y-2">
        {Object.entries(data).map(([key, value]) => {
          const display = value < 1 ? `${(value * 100).toFixed(0)}%` : value.toFixed(2);
          const barColor = value >= goodThreshold ? "bg-emerald-500" : value >= goodThreshold * 0.75 ? "bg-amber-500" : "bg-red-500";
          const textColor = value >= goodThreshold ? "text-emerald-600 dark:text-emerald-400" : value >= goodThreshold * 0.75 ? "text-amber-600 dark:text-amber-400" : "text-red-600 dark:text-red-400";
          return (
            <div key={key}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-surface-600 dark:text-surface-400 capitalize">{key.replace(/_/g, " ")}</span>
                <span className={`text-xs font-semibold ${textColor}`}>{display}</span>
              </div>
              <div className="w-full h-1.5 bg-surface-100 dark:bg-surface-800 rounded-full overflow-hidden">
                <div className={`h-full rounded-full ${barColor} transition-all duration-500`} style={{ width: `${Math.min(value * 100, 100)}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TargetIcon() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>; }
function ClockIcon() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>; }
function SearchIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>; }
function SparkleIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5z"/><line x1="19" y1="17" x2="19" y2="22"/><line x1="22" y1="19.5" x2="17" y2="19.5"/></svg>; }
function ChartIcon() { return <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>; }

export default Dashboard;
