import React, { useState } from 'react';
import {
  Sparkles,
  Flame,
  Bell,
  Sliders,
  X,
  Award,
  Cpu,
  GraduationCap,
  MessageSquare,
  Calculator,
  Terminal,
  BookOpen,
  History,
  BookmarkCheck,
  TrendingUp,
  Users
} from 'lucide-react';

export default function Header({
  stats,
  adaptiveLevel,
  activeTab,
  onOpenSettings,
  settings
}) {
  const [showNotifications, setShowNotifications] = useState(false);
  const streak = stats?.study_streak || 0;

  const tabTitles = {
    chat: { title: 'AI Academic Tutor', subtitle: 'On-the-fly multi-domain reasoning & SymPy verification', icon: MessageSquare },
    math: { title: 'Deterministic SymPy Studio', subtitle: 'Exact symbolic calculus, limits, and matrices', icon: Calculator },
    code: { title: 'Code Sandbox & AST', subtitle: 'AST static syntax audit & isolated subprocess runner', icon: Terminal },
    quiz: { title: 'Practice & Quizzes', subtitle: 'Conceptual MCQs, timer, and coding challenges', icon: BookOpen },
    history: { title: 'Learning History', subtitle: 'Searchable SQLite database of past doubt solutions', icon: History },
    study: { title: 'Study Hub & Notes', subtitle: 'Grounded RAG document QA and personal notebook', icon: BookmarkCheck },
    progress: { title: 'Student Analytics', subtitle: 'Weekly activity charts and conceptual mastery radar', icon: TrendingUp },
    faculty: { title: 'Faculty Dashboard', subtitle: 'Classroom misconception alerts and cohort reports', icon: Users }
  };

  const currentTabInfo = tabTitles[activeTab] || tabTitles.chat;
  const TabIcon = currentTabInfo.icon;

  const notifications = [
    {
      id: 1,
      title: 'Study Streak Active',
      desc: `You have an active ${streak}-day consecutive study streak!`,
      time: 'Today',
      icon: Flame,
      color: 'text-amber-400'
    },
    {
      id: 2,
      title: 'SymPy Math Engine v2.0 Active',
      desc: 'High-precision symbolic mathematics engine ready.',
      time: 'Live',
      icon: Cpu,
      color: 'text-[#22C8E5]'
    },
    {
      id: 3,
      title: 'Calibrated Pedagogical Level',
      desc: `Your current academic difficulty is set to ${settings.level || 'Intermediate'}.`,
      time: 'Active',
      icon: Award,
      color: 'text-[#7867FF]'
    }
  ];

  return (
    <header className="bg-[#0B0F1D]/80 backdrop-blur-md border-b border-white/10 px-5 sm:px-8 py-3 sticky top-0 z-30 transition-all">
      <div className="flex items-center justify-between gap-4">
        {/* Left: Active Workspace Breadcrumb */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-[#7867FF]/15 border border-[#7867FF]/30 text-[#7867FF] shrink-0">
            <TabIcon className="w-4 h-4" />
          </div>
          <div>
            <div className="text-sm font-bold text-white flex items-center gap-2">
              <span>{currentTabInfo.title}</span>
              <span className="hidden sm:inline-block w-1 h-1 rounded-full bg-slate-500"></span>
              <span className="hidden sm:inline text-xs font-normal text-slate-400">{currentTabInfo.subtitle}</span>
            </div>
          </div>
        </div>

        {/* Right: Actions, Streak, Tutor Settings, Notifications, Profile */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Study Streak Pill */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/25 text-amber-400 text-xs font-semibold">
            <Flame className="w-3.5 h-3.5 fill-amber-400" />
            <span>{streak} <span className="hidden md:inline font-normal text-slate-400">days</span></span>
          </div>

          {/* Tutor Settings Button */}
          <button
            onClick={onOpenSettings}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 hover:border-[#7867FF]/50 text-slate-300 hover:text-white transition-all text-xs font-medium"
            title="Configure Pedagogical Controls & AI Engine"
          >
            <Sliders className="w-3.5 h-3.5 text-[#22C8E5]" />
            <span className="hidden sm:inline">Settings</span>
            <span className="text-[10px] font-semibold text-[#22C8E5] bg-[#22C8E5]/15 px-1.5 py-0.2 rounded">
              {settings.level || 'Intermediate'}
            </span>
          </button>

          {/* Notifications Toggle */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:text-white hover:bg-white/10 transition-colors relative"
              title="Academic Notifications"
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

          {/* User Profile */}
          <div className="flex items-center gap-2 pl-2 border-l border-white/10">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#7867FF] to-[#22C8E5] p-[1px] shadow-sm">
              <div className="w-full h-full rounded-[11px] bg-[#0B0F1D] flex items-center justify-center text-xs font-bold text-white">
                SC
              </div>
            </div>
            <div className="hidden lg:block text-left">
              <div className="text-xs font-bold text-white leading-tight">Scholar</div>
              <div className="text-[10px] text-emerald-400 flex items-center gap-1 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Online
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
