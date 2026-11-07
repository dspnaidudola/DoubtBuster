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
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  Key,
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

  // UI state
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
    { id: 'chat', label: 'AI Tutor', icon: MessageSquare, badge: 'Core' },
    { id: 'math', label: 'Math Studio (SymPy)', icon: Calculator, badge: 'Verified' },
    { id: 'code', label: 'Code Sandbox & AST', icon: Terminal, badge: 'Isolated' },
    { id: 'quiz', label: 'Practice & Quizzes', icon: BookOpen, badge: null },
    { id: 'history', label: 'Learning History', icon: History, badge: null },
    { id: 'study', label: 'Study Hub & Notes', icon: BookmarkCheck, badge: 'RAG' },
    { id: 'progress', label: 'Student Analytics', icon: TrendingUp, badge: null },
    { id: 'faculty', label: 'Faculty Dashboard', icon: Users, badge: 'Admin' }
  ];

  const handleResetChat = () => {
    setMessages([]);
  };

  const handleSwitchTab = (tabId) => {
    setActiveTab(tabId);
    setMobileMenuOpen(false);
  };

  const sidebarSettings = {
    level,
    mode,
    language,
    attempt,
    apiKey,
    provider
  };

  return (
    <div className="flex min-h-screen bg-[#080B16] text-[#F8FAFC] font-sans antialiased">
      {/* Mobile Header Bar with Hamburger */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-14 bg-[#0D1222]/95 backdrop-blur-md border-b border-white/10 z-50 flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-[#7867FF]/20 text-[#7867FF]">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="font-extrabold text-gradient text-lg tracking-tight">DoubtBuster</span>
        </div>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-2 rounded-lg bg-white/5 text-slate-300 hover:text-white"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Drawer Overlay */}
      {mobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-40"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar Navigation */}
      <aside
        className={`fixed lg:sticky top-0 left-0 h-screen bg-[#0D1222] border-r border-white/10 p-4 shrink-0 flex flex-col justify-between z-40 transition-all duration-300 ${
          sidebarCollapsed ? 'lg:w-20' : 'lg:w-72'
        } ${
          mobileMenuOpen ? 'translate-x-0 w-72' : '-translate-x-full lg:translate-x-0'
        } overflow-y-auto`}
      >
        <div className="space-y-5">
          {/* Top Logo & Desktop Collapse Toggle */}
          <div className="flex items-center justify-between pt-2 lg:pt-0">
            <div className={`flex items-center gap-2.5 ${sidebarCollapsed ? 'justify-center w-full' : ''}`}>
              <div className="p-2 rounded-xl bg-gradient-to-br from-[#7867FF]/25 to-[#22C8E5]/25 border border-[#7867FF]/40 text-[#7867FF] shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>
              {!sidebarCollapsed && (
                <div>
                  <div className="text-lg font-extrabold tracking-tight text-gradient">
                    DoubtBuster
                  </div>
                  <div className="text-[10px] text-[#A1AEC4] tracking-wider uppercase font-semibold">
                    Universal AI Academic
                  </div>
                </div>
              )}
            </div>

            {/* Desktop Collapse Button */}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="hidden lg:flex p-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition-colors"
              title={sidebarCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
            >
              {sidebarCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>

          {/* New Chat / Reset Button */}
          <button
            onClick={handleResetChat}
            className={`btn-primary w-full py-2.5 px-3 text-xs flex items-center justify-center gap-2 font-semibold ${
              sidebarCollapsed ? 'px-2' : ''
            }`}
            title="Reset Chat / New Doubt"
          >
            <RotateCcw className="w-4 h-4 shrink-0" />
            {!sidebarCollapsed && <span>New Chat / Reset</span>}
          </button>

          {/* Navigation Items */}
          <nav className="space-y-1">
            {!sidebarCollapsed && (
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 mb-2">
                Workspace Modules
              </div>
            )}
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleSwitchTab(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-[#7867FF] to-[#604CEE] text-white shadow-lg shadow-[#7867FF]/25'
                      : 'text-[#A1AEC4] hover:text-white hover:bg-white/5'
                  } ${sidebarCollapsed ? 'justify-center px-0' : ''}`}
                  title={item.label}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-[#A1AEC4]'}`} />
                  {!sidebarCollapsed && (
                    <div className="flex-1 text-left flex items-center justify-between">
                      <span className="truncate">{item.label}</span>
                      {item.badge && (
                        <span className={`text-[9px] px-1.5 py-0.2 rounded font-semibold ${
                          isActive
                            ? 'bg-white/20 text-white'
                            : 'bg-white/5 text-slate-400'
                        }`}>
                          {item.badge}
                        </span>
                      )}
                    </div>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Pedagogical Controls Section */}
          {!sidebarCollapsed && (
            <div className="pt-4 border-t border-white/10 space-y-3.5">
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5 px-1">
                <Sliders className="w-3.5 h-3.5 text-[#22C8E5]" />
                <span>Pedagogical Controls</span>
              </div>

              <div>
                <label className="block text-[11px] text-slate-400 mb-1">
                  Skill Level (Adaptive: <strong className="text-[#22C8E5]">{adaptiveLevel}</strong>)
                </label>
                <select
                  value={level}
                  onChange={(e) => setLevel(e.target.value)}
                  className="w-full text-xs py-1.5 bg-[#141B2D]"
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
                  className="w-full text-xs py-1.5 bg-[#141B2D]"
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
                    className="w-full text-xs bg-[#141B2D]"
                  />
                </div>
              )}

              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Response Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full text-xs py-1.5 bg-[#141B2D]"
                >
                  <option>English</option>
                  <option>Simple English</option>
                  <option>Telugu (Technical mix)</option>
                  <option>Hindi (Technical mix)</option>
                </select>
              </div>

              {/* AI Engine Provider */}
              <div className="pt-2 border-t border-white/5 space-y-2">
                <label className="block text-[11px] text-slate-400 flex items-center justify-between">
                  <span>AI Engine Provider</span>
                  <Settings className="w-3 h-3 text-slate-500" />
                </label>
                <select
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="w-full text-xs py-1.5 bg-[#141B2D]"
                >
                  <option value="offline">Auto-detect / Free Built-in Mode</option>
                  <option value="gemini">Google Gemini 2.0</option>
                  <option value="groq">Groq Llama-3.3-70B</option>
                  <option value="openai">OpenAI GPT-4o-mini</option>
                </select>

                {provider !== 'offline' && (
                  <div className="pt-1">
                    <input
                      type="password"
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      placeholder={`Enter ${provider} API Key`}
                      className="w-full text-xs py-1.5 bg-[#141B2D]"
                    />
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar Footer */}
        {!sidebarCollapsed && (
          <div className="pt-4 border-t border-white/10 text-[11px] text-slate-500 flex flex-col gap-1">
            <div className="flex items-center gap-1.5 text-slate-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>DoubtBuster 2.0 • Active</span>
            </div>
            <div className="text-[10px] text-slate-500">
              Department of CSE • GMRIT
            </div>
          </div>
        )}
      </aside>

      {/* Main Content Workspace */}
      <main className="flex-1 flex flex-col min-w-0 pt-14 lg:pt-0">
        <Header
          stats={stats}
          adaptiveLevel={adaptiveLevel}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
        />

        <div className="p-4 sm:p-6 lg:p-8 flex-1 overflow-x-hidden">
          {activeTab === 'chat' && (
            <ChatTab
              messages={messages}
              setMessages={setMessages}
              settings={sidebarSettings}
              stats={stats}
              onRefreshStats={fetchStats}
            />
          )}

          {activeTab === 'math' && <MathTab />}

          {activeTab === 'code' && <CodeTab />}

          {activeTab === 'quiz' && <QuizTab onRefreshStats={fetchStats} />}

          {activeTab === 'history' && (
            <HistoryTab
              onContinueInChat={(question, answer) => {
                setMessages([
                  {
                    role: 'user',
                    content: question,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                  },
                  {
                    role: 'assistant',
                    content: answer,
                    field: 'History Recall',
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                  }
                ]);
                setActiveTab('chat');
              }}
            />
          )}

          {activeTab === 'study' && <StudyTab />}

          {activeTab === 'progress' && (
            <ProgressTab stats={stats} onRefreshStats={fetchStats} />
          )}

          {activeTab === 'faculty' && <FacultyTab />}
        </div>
      </main>
    </div>
  );
}
