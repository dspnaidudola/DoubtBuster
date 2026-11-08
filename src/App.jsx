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
  ShieldCheck,
  Cpu
} from 'lucide-react';

import Header from './components/Header';
import SettingsModal from './components/SettingsModal';
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

  // Pedagogical & Provider Settings State
  const [settings, setSettings] = useState({
    level: 'Intermediate',
    mode: 'Step-by-step explanation',
    language: 'English',
    attempt: '',
    provider: 'offline',
    apiKey: ''
  });

  // UI state
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [settingsModalOpen, setSettingsModalOpen] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      setStats(data.stats || {});
      setAdaptiveLevel(data.adaptive_difficulty || 'Intermediate');
      setSettings((prev) => ({
        ...prev,
        level: data.adaptive_difficulty || prev.level
      }));
    } catch (e) {
      console.error('Could not fetch stats:', e);
    }
  };

  const navItems = [
    { id: 'chat', label: 'AI Academic Tutor', icon: MessageSquare },
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
    setActiveTab('chat');
  };

  const handleSwitchTab = (tabId) => {
    setActiveTab(tabId);
    setMobileMenuOpen(false);
  };

  return (
    <div className="flex min-h-screen bg-[#070913] text-[#F8FAFC] font-sans antialiased">
      {/* Mobile Top Bar */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-14 bg-[#0B0F1D]/95 backdrop-blur-md border-b border-white/10 z-40 flex items-center justify-between px-4">
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

      {/* Mobile Drawer Backdrop */}
      {mobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/75 backdrop-blur-sm z-40"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar Navigation */}
      <aside
        className={`fixed lg:sticky top-0 left-0 h-screen bg-[#0B0F1D] border-r border-white/10 p-4 shrink-0 flex flex-col justify-between z-40 transition-all duration-300 ${
          sidebarCollapsed ? 'lg:w-20' : 'lg:w-68'
        } ${
          mobileMenuOpen ? 'translate-x-0 w-72' : '-translate-x-full lg:translate-x-0'
        } overflow-y-auto`}
      >
        <div className="space-y-5">
          {/* Top Logo & Desktop Collapse Toggle */}
          <div className="flex items-center justify-between pt-2 lg:pt-0">
            <div className={`flex items-center gap-2.5 ${sidebarCollapsed ? 'justify-center w-full' : ''}`}>
              <div className="p-2 rounded-xl bg-gradient-to-br from-[#7867FF]/25 to-[#22C8E5]/25 border border-[#7867FF]/35 text-[#7867FF] shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>
              {!sidebarCollapsed && (
                <div>
                  <div className="text-lg font-extrabold tracking-tight text-gradient">
                    DoubtBuster
                  </div>
                  <div className="text-[10px] text-[#94A3B8] tracking-wider uppercase font-semibold">
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

          {/* New Chat Button */}
          <button
            onClick={handleResetChat}
            className={`btn-primary w-full py-2.5 px-3 text-xs flex items-center justify-center gap-2 font-semibold shadow-md ${
              sidebarCollapsed ? 'px-2' : ''
            }`}
            title="Start New Academic Dialogue"
          >
            <RotateCcw className="w-4 h-4 shrink-0" />
            {!sidebarCollapsed && <span>New Doubt / Reset</span>}
          </button>

          {/* Navigation Links */}
          <nav className="space-y-1.5">
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
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-[#7867FF] to-[#604CEE] text-white shadow-lg shadow-[#7867FF]/30'
                      : 'text-[#94A3B8] hover:text-white hover:bg-white/5'
                  } ${sidebarCollapsed ? 'justify-center px-0' : ''}`}
                  title={item.label}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-[#94A3B8]'}`} />
                  {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Sidebar Bottom Controls */}
        <div className="pt-4 border-t border-white/10 space-y-3">
          {/* Quick Settings Trigger Card */}
          {!sidebarCollapsed ? (
            <div
              onClick={() => setSettingsModalOpen(true)}
              className="p-3 rounded-xl bg-white/5 border border-white/5 hover:border-[#7867FF]/40 cursor-pointer transition-all space-y-1.5 group"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-300 font-semibold flex items-center gap-1.5 group-hover:text-white">
                  <Sliders className="w-3.5 h-3.5 text-[#22C8E5]" /> Tutor Controls
                </span>
                <span className="text-[10px] text-[#22C8E5] font-bold bg-[#22C8E5]/15 px-1.5 py-0.2 rounded">
                  {settings.level}
                </span>
              </div>
              <div className="text-[10px] text-slate-400 truncate">
                Mode: {settings.mode}
              </div>
            </div>
          ) : (
            <button
              onClick={() => setSettingsModalOpen(true)}
              className="w-full p-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white flex items-center justify-center transition-colors"
              title="Tutor Controls"
            >
              <Sliders className="w-4 h-4 text-[#22C8E5]" />
            </button>
          )}

          {/* Department Footer */}
          {!sidebarCollapsed && (
            <div className="text-[10px] text-slate-500 px-1 flex flex-col gap-0.5">
              <div className="flex items-center gap-1.5 text-slate-400 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>DoubtBuster v2.0 • Active</span>
              </div>
              <div>Department of CSE • GMRIT</div>
            </div>
          )}
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main className="flex-1 flex flex-col min-w-0 pt-14 lg:pt-0">
        <Header
          stats={stats}
          adaptiveLevel={adaptiveLevel}
          activeTab={activeTab}
          onOpenSettings={() => setSettingsModalOpen(true)}
          settings={settings}
        />

        <div className="p-4 sm:p-6 lg:p-8 flex-1 overflow-x-hidden">
          {activeTab === 'chat' && (
            <ChatTab
              messages={messages}
              setMessages={setMessages}
              settings={settings}
              stats={stats}
              onRefreshStats={fetchStats}
              onOpenSettings={() => setSettingsModalOpen(true)}
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

      {/* Tutor Settings Modal */}
      <SettingsModal
        isOpen={settingsModalOpen}
        onClose={() => setSettingsModalOpen(false)}
        settings={settings}
        onUpdateSettings={(newSettings) => setSettings(newSettings)}
        adaptiveLevel={adaptiveLevel}
      />
    </div>
  );
}
