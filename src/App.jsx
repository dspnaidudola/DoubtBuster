import React, { useState, useEffect } from 'react';
import {
  MessageSquare,
  Calculator,
  Terminal,
  BookOpen,
  History,
  BookmarkCheck,
  TrendingUp,
  Users,
  RotateCcw,
  Sliders,
  Settings,
  Sparkles,
  ShieldCheck,
  Cpu
} from 'lucide-react';

import Header from './components/Header';
import ChatTab from './components/ChatTab';
import MathTab from './components/MathTab';
import CodeTab from './components/CodeTab';
import QuizTab from './components/QuizTab';
import HistoryTab from './components/HistoryTab';
import StudyTab from './components/StudyTab';
import ProgressTab from './components/ProgressTab';
import FacultyTab from './components/FacultyTab';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState(null);
  const [adaptiveLevel, setAdaptiveLevel] = useState('Intermediate');

  // Sidebar settings state
  const [level, setLevel] = useState('Intermediate');
  const [mode, setMode] = useState('Step-by-step explanation');
  const [language, setLanguage] = useState('English');
  const [attempt, setAttempt] = useState('');
  const [provider, setProvider] = useState('offline');
  const [apiKey, setApiKey] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      setStats(data.stats || {});
      setAdaptiveLevel(data.adaptive_difficulty || 'Intermediate');
      setLevel(data.adaptive_difficulty || 'Intermediate');
    } catch (e) {
      console.error('Could not fetch stats:', e);
    }
  };

  const navItems = [
    { id: 'chat', label: 'Ask AI Tutor', icon: MessageSquare },
    { id: 'math', label: 'Math Studio (SymPy)', icon: Calculator },
    { id: 'code', label: 'Code Sandbox & AST', icon: Terminal },
    { id: 'quiz', label: 'Practice & Quizzes', icon: BookOpen },
    { id: 'history', label: 'Learning History', icon: History },
    { id: 'study', label: 'Study Hub & Notes', icon: BookmarkCheck },
    { id: 'progress', label: 'Student Analytics', icon: TrendingUp },
    { id: 'faculty', label: 'Faculty Dashboard', icon: Users }
  ];

  const handleResetChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex flex-col lg:flex-row min-h-screen bg-[#070913] text-slate-100">
      {/* Sidebar Controls */}
      <aside className="w-full lg:w-72 bg-[#090d1a] border-r border-white/10 p-5 shrink-0 flex flex-col justify-between space-y-6">
        <div className="space-y-6">
          {/* Logo & Reset */}
          <div>
            <div className="flex items-center gap-2.5 mb-1">
              <span className="p-1.5 rounded-lg bg-indigo-500/20 text-indigo-400">
                <Sparkles className="w-5 h-5" />
              </span>
              <span className="text-xl font-extrabold tracking-tight text-gradient">
                DoubtBuster
              </span>
            </div>
            <div className="text-[11px] text-slate-400">
              Universal Academic Companion v2.0
            </div>

            <button
              onClick={handleResetChat}
              className="btn-primary w-full mt-4 py-2 px-3 text-xs flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>New Chat / Reset</span>
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1">
            <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 mb-2">
              Workspace Modules
            </div>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-lg shadow-indigo-600/30'
                      : 'text-slate-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Pedagogical Controls */}
          <div className="pt-4 border-t border-white/10 space-y-3.5">
            <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <Sliders className="w-3 h-3 text-sky-400" />
              <span>Pedagogical Controls</span>
            </div>

            <div>
              <label className="block text-[11px] text-slate-400 mb-1">
                Skill Level (Adaptive: <strong className="text-sky-400">{adaptiveLevel}</strong>)
              </label>
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                className="w-full text-xs py-1.5"
              >
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] text-slate-400 mb-1">Pedagogical Mode</label>
              <select
                value={mode}
                onChange={(e) => setMode(e.target.value)}
                className="w-full text-xs py-1.5"
              >
                <option>Step-by-step explanation</option>
                <option>Hint first</option>
                <option>Verify my answer</option>
                <option>Practice question with answer key</option>
              </select>
            </div>

            {mode === 'Verify my answer' && (
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Your Preliminary Attempt</label>
                <textarea
                  rows={2}
                  value={attempt}
                  onChange={(e) => setAttempt(e.target.value)}
                  placeholder="Type your reasoning..."
                  className="w-full text-xs"
                />
              </div>
            )}

            <div>
              <label className="block text-[11px] text-slate-400 mb-1">Response Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full text-xs py-1.5"
              >
                <option>English</option>
                <option>Simple English</option>
                <option>Telugu (Technical mix)</option>
                <option>Hindi (Technical mix)</option>
              </select>
            </div>
          </div>

          {/* AI Engine Provider */}
          <div className="pt-4 border-t border-white/10 space-y-3">
            <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <Settings className="w-3 h-3 text-violet-400" />
              <span>AI Provider & Key</span>
            </div>

            <div>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full text-xs py-1.5"
              >
                <option value="offline">Auto-detect / Free Built-in Mode</option>
                <option value="gemini">Google Gemini (2.5 Flash)</option>
                <option value="openai">OpenAI (GPT-4o)</option>
                <option value="groq">Groq (LLaMA-3.3)</option>
              </select>
            </div>

            {provider !== 'offline' && (
              <div>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Enter API key..."
                  className="w-full text-xs py-1.5"
                />
              </div>
            )}

            <div className="text-[10px] text-slate-500 leading-relaxed">
              {provider === 'offline'
                ? '💡 Free zero-cost built-in pedagogical tutor with SymPy engine active.'
                : '🟢 Connected to custom cloud API provider.'}
            </div>
          </div>
        </div>

        {/* Footer Attribution */}
        <div className="pt-4 border-t border-white/10 text-[10px] text-slate-500">
          Project 14 • Department of CSE • GMRIT
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main className="flex-1 p-5 md:p-8 overflow-y-auto">
        <Header stats={stats} adaptiveLevel={adaptiveLevel} />

        {/* Tab Views */}
        <div className="max-w-7xl mx-auto">
          {activeTab === 'chat' && (
            <ChatTab
              messages={messages}
              setMessages={setMessages}
              settings={{ level, mode, language, attempt, apiKey, model: provider }}
              onRefreshStats={fetchStats}
            />
          )}

          {activeTab === 'math' && <MathTab />}

          {activeTab === 'code' && <CodeTab />}

          {activeTab === 'quiz' && <QuizTab />}

          {activeTab === 'history' && <HistoryTab />}

          {activeTab === 'study' && <StudyTab />}

          {activeTab === 'progress' && <ProgressTab stats={stats} onRefreshStats={fetchStats} />}

          {activeTab === 'faculty' && <FacultyTab />}
        </div>
      </main>
    </div>
  );
}
