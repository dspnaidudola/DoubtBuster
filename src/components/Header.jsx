import React from 'react';
import { Sparkles, Flame, CheckCircle2, ShieldCheck, Terminal, Cpu } from 'lucide-react';

export default function Header({ stats, adaptiveLevel }) {
  const streak = stats?.study_streak || 0;
  const doubtsCount = stats?.total_doubts || 0;

  return (
    <div className="hero-gradient p-6 md:p-8 mb-6 relative overflow-hidden">
      {/* Background soft glow accent */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative z-10">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="p-2 bg-indigo-500/15 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Sparkles className="w-6 h-6 animate-pulse" />
            </span>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-gradient">
              DoubtBuster
            </h1>
          </div>
          
          <p className="text-slate-400 text-sm md:text-base max-w-2xl font-normal leading-relaxed">
            Universal AI Academic Tutor — On-the-fly multi-domain reasoning, SymPy mathematical verification, and isolated sandbox execution.
          </p>

          <div className="flex flex-wrap gap-2 mt-4">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white/5 border border-white/10 text-slate-300 flex items-center gap-1.5 backdrop-blur-md">
              <CheckCircle2 className="w-3.5 h-3.5 text-sky-400" />
              Dynamic Synthesis (Zero Hallucinations)
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white/5 border border-white/10 text-slate-300 flex items-center gap-1.5 backdrop-blur-md">
              <Cpu className="w-3.5 h-3.5 text-violet-400" />
              SymPy Math Engine
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white/5 border border-white/10 text-slate-300 flex items-center gap-1.5 backdrop-blur-md">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              Secure Subprocess Sandbox
            </span>
            {adaptiveLevel && (
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-sky-500/15 border border-sky-500/30 text-sky-300 flex items-center gap-1.5 backdrop-blur-md">
                🎯 Level: {adaptiveLevel}
              </span>
            )}
          </div>
        </div>

        {/* Study Streak & Activity Pill */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-4 text-center min-w-[150px] backdrop-blur-lg shadow-inner">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Study Streak
          </div>
          <div className="text-3xl font-extrabold text-sky-400 flex items-center justify-center gap-1.5 my-1">
            <Flame className="w-6 h-6 text-amber-400 fill-amber-400" />
            {streak} <span className="text-xs font-medium text-slate-400">days</span>
          </div>
          <div className="text-[11px] text-slate-500">
            {doubtsCount} doubts resolved
          </div>
        </div>
      </div>
    </div>
  );
}

