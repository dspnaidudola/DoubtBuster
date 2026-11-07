import React, { useState } from 'react';
import {
  Sparkles,
  Flame,
  Bell,
  ShieldCheck,
  CheckCircle2,
  Cpu,
  GraduationCap,
  X,
  BookOpen,
  Award
} from 'lucide-react';

export default function Header({
  stats,
  adaptiveLevel,
  activeTab,
  setActiveTab
}) {
  const [showNotifications, setShowNotifications] = useState(false);
  const streak = stats?.study_streak || 0;
  const doubtsCount = stats?.total_doubts || 0;

  const notifications = [
    {
      id: 1,
      title: 'Daily Study Streak Active',
      desc: `You have an active ${streak}-day learning streak. Keep practicing!`,
      time: 'Just now',
      icon: Flame,
      color: 'text-amber-400'
    },
    {
      id: 2,
      title: 'SymPy Math Engine v2.0 Ready',
      desc: 'Deterministic calculus and matrix verification active with zero hallucinations.',
      time: '5m ago',
      icon: Cpu,
      color: 'text-[#22C8E5]'
    },
    {
      id: 3,
      title: 'Adaptive Difficulty Configured',
      desc: `Your current academic level is calibrated to ${adaptiveLevel}.`,
      time: 'Today',
      icon: Award,
      color: 'text-[#7867FF]'
    }
  ];

  return (
    <header className="bg-[#0D1222]/90 backdrop-blur-md border-b border-white/10 px-6 py-3.5 sticky top-0 z-40 transition-all">
      <div className="flex items-center justify-between gap-4">
        {/* Left: Branding & Tagline */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-br from-[#7867FF]/20 to-[#22C8E5]/20 border border-[#7867FF]/35 text-[#7867FF]">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-extrabold tracking-tight text-gradient">
                DoubtBuster
              </h1>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#7867FF]/15 border border-[#7867FF]/30 text-[#7867FF]">
                v2.0
              </span>
            </div>
            <div className="text-[11px] text-[#A1AEC4] hidden sm:block">
              Universal AI Academic Companion
            </div>
          </div>
        </div>

        {/* Center: Quick Welcome */}
        <div className="hidden md:flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-slate-300">
          <GraduationCap className="w-4 h-4 text-[#22C8E5]" />
          <span>Welcome back, <strong className="text-white">Scholar</strong></span>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse ml-1"></span>
        </div>

        {/* Right: Actions, Streak, Notifications & Profile */}
        <div className="flex items-center gap-3">
          {/* Study Streak Pill */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/25 text-amber-400 text-xs font-semibold">
            <Flame className="w-4 h-4 fill-amber-400" />
            <span>{streak} <span className="hidden sm:inline font-normal text-slate-400">days streak</span></span>
          </div>

          {/* Notifications Toggle */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:text-white hover:bg-white/10 transition-colors relative"
              title="Notifications"
            >
              <Bell className="w-4 h-4" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#22C8E5]"></span>
            </button>

            {/* Notification Dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 sm:w-96 glass-card p-4 shadow-2xl z-50 border border-white/15 animate-slide-up">
                <div className="flex justify-between items-center pb-3 border-b border-white/10 mb-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-white uppercase tracking-wider">
                    <Bell className="w-3.5 h-3.5 text-[#22C8E5]" />
                    <span>Academic Notifications</span>
                  </div>
                  <button
                    onClick={() => setShowNotifications(false)}
                    className="text-slate-400 hover:text-white text-xs"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="space-y-2.5">
                  {notifications.map((n) => {
                    const Icon = n.icon;
                    return (
                      <div
                        key={n.id}
                        className="p-2.5 rounded-xl bg-white/5 border border-white/5 hover:border-white/10 transition-colors flex gap-3 items-start"
                      >
                        <div className={`p-1.5 rounded-lg bg-black/30 ${n.color} shrink-0`}>
                          <Icon className="w-4 h-4" />
                        </div>
                        <div className="flex-1">
                          <div className="text-xs font-semibold text-white flex justify-between">
                            <span>{n.title}</span>
                            <span className="text-[10px] text-slate-400 font-normal">{n.time}</span>
                          </div>
                          <div className="text-[11px] text-slate-300 mt-0.5 leading-snug">
                            {n.desc}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* User Profile Pill */}
          <div className="flex items-center gap-2 pl-2 border-l border-white/10">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#7867FF] to-[#22C8E5] p-[1px] shadow-sm">
              <div className="w-full h-full rounded-[11px] bg-[#0D1222] flex items-center justify-center text-xs font-bold text-white">
                SC
              </div>
            </div>
            <div className="hidden lg:block text-left">
              <div className="text-xs font-bold text-white leading-tight">Scholar</div>
              <div className="text-[10px] text-emerald-400 flex items-center gap-1 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> GMRIT • Level: {adaptiveLevel}
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
