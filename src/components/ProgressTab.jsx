import React, { useState } from 'react';
import { Flame, Award, BookOpen, Terminal, ShieldAlert, CheckCircle2, Trash2 } from 'lucide-react';

export default function ProgressTab({ stats, onRefreshStats }) {
  const [purgeLoading, setPurgeLoading] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const totalDoubts = stats?.total_doubts || 0;
  const totalQuizzes = stats?.total_quizzes || 0;
  const avgScore = stats?.avg_quiz_score || 0.0;
  const streak = stats?.study_streak || 0;
  const totalCoding = stats?.total_coding || 0;
  const passedCoding = stats?.passed_coding || 0;

  const subjectCounts = stats?.subject_counts || {};
  const quizStats = stats?.quiz_subject_stats || {};

  const handlePurge = async () => {
    setPurgeLoading(true);
    try {
      await fetch('/api/stats/purge', { method: 'POST' });
      setShowConfirm(false);
      if (onRefreshStats) onRefreshStats();
    } catch (e) {
      console.error(e);
    } finally {
      setPurgeLoading(false);
    }
  };

  const disciplines = [
    "Computer Science & Programming",
    "Mathematics & Statistics",
    "AI, Machine Learning & Data Science",
    "Computer Architecture & Microprocessors",
    "Electrical & Electronics Engineering",
    "Physics & Physical Sciences"
  ];

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="kpi-card">
          <div className="kpi-label">Doubts Resolved</div>
          <div className="kpi-value text-sky-400">{totalDoubts}</div>
          <div className="text-[11px] text-emerald-400 font-semibold">Persistent local logging</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Quizzes Completed</div>
          <div className="kpi-value text-indigo-400">{totalQuizzes}</div>
          <div className="text-[11px] text-slate-400">Avg {avgScore}% accuracy</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Coding Challenges</div>
          <div className="kpi-value text-rose-400">{passedCoding}/{totalCoding}</div>
          <div className="text-[11px] text-slate-400">Verified in sandbox</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Active Study Streak</div>
          <div className="kpi-value text-amber-400 flex items-center justify-center gap-1">
            <Flame className="w-6 h-6 fill-amber-400 text-amber-400" />
            {streak}
          </div>
          <div className="text-[11px] text-slate-400">Consecutive days active</div>
        </div>
      </div>

      {/* Subject Doubts Distribution */}
      <div className="glass-card p-6 space-y-4">
        <h4 className="text-sm font-bold text-white">📊 Doubts Resolved by Academic Discipline</h4>
        {Object.keys(subjectCounts).length === 0 ? (
          <div className="text-xs text-slate-400 py-4">No doubts logged yet. Start asking in AI Tutor tab!</div>
        ) : (
          <div className="space-y-3">
            {Object.entries(subjectCounts).map(([subj, count], i) => {
              const maxCount = Math.max(...Object.values(subjectCounts), 1);
              const pct = Math.round((count / maxCount) * 100);

              return (
                <div key={i} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-semibold">{subj}</span>
                    <span className="text-sky-400 font-bold">{count} doubts</span>
                  </div>
                  <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-sky-500 to-indigo-500 rounded-full transition-all duration-500"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Academic Mastery Matrix */}
      <div className="glass-card p-6 space-y-4">
        <h4 className="text-sm font-bold text-white">🏅 Academic Mastery Matrix</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {disciplines.map((subj, idx) => {
            const dCount = subjectCounts[subj] || 0;
            const qInfo = quizStats[subj] || { avg_score: 0.0, count: 0 };
            const qScore = qInfo.avg_score;

            let levelText = 'Not Started';
            let badgeBg = 'bg-slate-700 text-slate-300';
            let barWidth = '5%';

            if (dCount > 0 || qInfo.count > 0) {
              if (dCount >= 5 && qScore >= 75) {
                levelText = 'Proficient';
                badgeBg = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
                barWidth = '95%';
              } else if (dCount >= 3 || qScore >= 60) {
                levelText = 'Developing';
                badgeBg = 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
                barWidth = '65%';
              } else {
                levelText = 'Novice';
                badgeBg = 'bg-sky-500/20 text-sky-300 border border-sky-500/30';
                barWidth = '30%';
              }
            }

            return (
              <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-white">{subj}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${badgeBg}`}>
                    {levelText}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400">
                  {dCount} doubts • {qInfo.count} quizzes ({qScore}%)
                </div>
                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full"
                    style={{ width: barWidth }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Privacy Data Controls */}
      <div className="glass-card p-6 border-rose-500/30 bg-rose-950/10 space-y-3">
        <h4 className="text-sm font-bold text-rose-300 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          Student Privacy & Local Data Management
        </h4>
        <p className="text-xs text-slate-400 leading-relaxed">
          All student activity, doubts, notes, and quiz metrics are persisted strictly on your local machine in SQLite with 0 external telemetry. You can purge all data at any time with 1 click.
        </p>

        {!showConfirm ? (
          <button
            onClick={() => setShowConfirm(true)}
            className="btn-secondary text-xs text-rose-400 hover:text-rose-300 border-rose-500/30"
          >
            <Trash2 className="w-3.5 h-3.5" /> Purge All Local Student Data
          </button>
        ) : (
          <div className="flex items-center gap-3 p-3 rounded-xl bg-rose-500/20 border border-rose-500/40">
            <span className="text-xs text-rose-200">
              Are you sure? This will permanently delete your doubts, quizzes, and notes from SQLite.
            </span>
            <button
              onClick={handlePurge}
              disabled={purgeLoading}
              className="btn-primary py-1 px-3 text-xs bg-rose-600 hover:bg-rose-700"
            >
              {purgeLoading ? 'Purging...' : 'Yes, Delete Everything'}
            </button>
            <button
              onClick={() => setShowConfirm(false)}
              className="btn-secondary py-1 px-3 text-xs"
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

