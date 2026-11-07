import React, { useState, useEffect } from 'react';
import { Users, AlertTriangle, Lightbulb, Download, BarChart2, CheckCircle2 } from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

export default function FacultyTab() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/faculty/analytics');
      const data = await res.json();
      setAnalytics(data.analytics || null);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!analytics) return;

    let md = `# GMRIT Faculty Analytics & Intervention Report\nGenerated: ${new Date().toLocaleString()}\nCohort: AY 2026-2027\n\n`;
    md += `## Cohort Summary\n`;
    md += `- **Total Student Doubts Logged:** ${analytics.total_queries}\n`;
    md += `- **High-Difficulty Flags:** ${analytics.challenging_topics?.length || 0}\n`;
    md += `- **Distinct Topics Tracked:** ${analytics.frequent_topics?.length || 0}\n\n`;

    md += `## Recommended Classroom Pedagogical Interventions\n`;
    (analytics.suggested_interventions || []).forEach((inter, i) => {
      md += `${i + 1}. ${inter}\n`;
    });

    md += `\n## Most Frequently Asked Topics\n`;
    (analytics.frequent_topics || []).forEach((t) => {
      md += `- **${t.topic}** (${t.subject}): ${t.query_count} inquiries\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `gmrit_faculty_report_${new Date().toISOString().slice(0, 10)}.md`;
    link.click();
  };

  if (loading || !analytics) {
    return <div className="text-center py-10 text-slate-400 text-sm">Loading faculty cohort analytics...</div>;
  }

  const avgScore = analytics.quiz_performance?.length
    ? Math.round(
        analytics.quiz_performance.reduce((acc, q) => acc + q.avg_score, 0) /
          analytics.quiz_performance.length
      )
    : 0;

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-indigo-400" />
            Faculty Analytics & Classroom Intervention Dashboard
          </h3>
          <p className="text-slate-400 text-xs md:text-sm mt-0.5">
            Identify cohort misconceptions, monitor difficult topic flags, and discover data-driven areas for classroom instruction.
          </p>
        </div>
        <button onClick={handleDownloadReport} className="btn-secondary text-xs">
          <Download className="w-3.5 h-3.5" /> Export Faculty Report
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="kpi-card">
          <div className="kpi-label">Total Student Inquiries</div>
          <div className="kpi-value text-sky-400">{analytics.total_queries}</div>
          <div className="text-[11px] text-slate-400">Aggregated cohort queries</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">High-Difficulty Flags</div>
          <div className="kpi-value text-rose-400">{analytics.challenging_topics?.length || 0}</div>
          <div className="text-[11px] text-rose-300">Concepts needing review</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Cohort Quiz Mastery</div>
          <div className="kpi-value text-emerald-400">{avgScore}%</div>
          <div className="text-[11px] text-slate-400">Across all quiz attempts</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Distinct Topics Tracked</div>
          <div className="kpi-value text-indigo-400">{analytics.frequent_topics?.length || 0}</div>
          <div className="text-[11px] text-slate-400">Active curriculum areas</div>
        </div>
      </div>

      {/* Recommended Classroom Pedagogical Interventions */}
      <div className="glass-card p-6 border-indigo-500/30 bg-indigo-950/15 space-y-3">
        <h4 className="text-sm font-bold text-white flex items-center gap-2">
          <Lightbulb className="w-4 h-4 text-amber-400" />
          Recommended Classroom Interventions for Faculty
        </h4>
        <p className="text-xs text-slate-300">
          AI-aggregated guidance based on frequent doubts, negative ratings, and student difficulty tags:
        </p>
        <div className="space-y-2 pt-1">
          {analytics.suggested_interventions?.length > 0 ? (
            analytics.suggested_interventions.map((inter, i) => (
              <div
                key={i}
                className="p-3 rounded-xl bg-slate-900/60 border border-amber-500/20 text-xs text-amber-200/90 flex items-start gap-2.5"
              >
                <span className="text-amber-400 font-bold shrink-0">📌</span>
                <span>{inter}</span>
              </div>
            ))
          ) : (
            <div className="text-xs text-slate-400">No urgent interventions required. Student mastery is currently stable.</div>
          )}
        </div>
      </div>

      {/* Topics Breakdown Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Most Frequent Topics */}
        <div className="glass-card p-6 space-y-4">
          <h4 className="text-sm font-bold text-white flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-sky-400" />
            Most Frequently Asked Topics
          </h4>
          {analytics.frequent_topics?.length === 0 ? (
            <div className="text-xs text-slate-400">No query data recorded yet.</div>
          ) : (
            <div className="space-y-2.5">
              {analytics.frequent_topics.map((t, i) => (
                <div
                  key={i}
                  className="flex justify-between items-center p-3 rounded-lg bg-slate-900/50 border border-white/5 text-xs"
                >
                  <div>
                    <strong className="text-white">{t.topic}</strong>
                    <div className="text-[11px] text-slate-400">{t.subject}</div>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-sky-500/15 text-sky-400 font-bold">
                    {t.query_count} inquiries
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Challenging Topics */}
        <div className="glass-card p-6 space-y-4">
          <h4 className="text-sm font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            Topics Flagged as Difficult by Students
          </h4>
          {analytics.challenging_topics?.length === 0 ? (
            <div className="text-xs text-slate-400">No topics flagged as difficult yet.</div>
          ) : (
            <div className="space-y-2.5">
              {analytics.challenging_topics.map((t, i) => (
                <div
                  key={i}
                  className="flex justify-between items-center p-3 rounded-lg bg-slate-900/50 border border-white/5 text-xs"
                >
                  <div>
                    <strong className="text-white">{t.topic}</strong>
                    <div className="text-[11px] text-slate-400">{t.subject}</div>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-rose-500/15 text-rose-400 font-bold">
                    Flagged {t.cnt} times
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
