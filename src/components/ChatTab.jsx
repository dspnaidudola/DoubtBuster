import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Bookmark,
  Flag,
  ThumbsUp,
  ThumbsDown,
  Brain,
  Copy,
  Check,
  Sparkles,
  User,
  CornerDownLeft,
  RotateCcw,
  Download,
  Mic,
  MicOff,
  Paperclip,
  X,
  HelpCircle,
  Clock,
  Flame,
  CheckCircle2,
  Terminal,
  Cpu,
  Calculator,
  Code2,
  Atom,
  ArrowRight,
  ChevronRight,
  Sliders
} from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

const SUBJECT_EXPLORATION_CARDS = [
  {
    id: 'cs',
    domain: 'Computer Science',
    title: 'Computer Science',
    icon: Terminal,
    color: 'from-sky-500/20 to-blue-600/10 text-sky-400 border-sky-500/30',
    description: 'Systems programming, Operating systems, Memory segmentation, CPU pipelining, and Networking architectures.',
    example: 'Explain Intel 8086 microprocessor internal architecture, BIU vs EU, and memory segmentation.',
    prompt: 'Explain the Intel 8086 microprocessor internal architecture, detailing the difference between the BIU and EU, 6-byte instruction queue, and memory segmentation.'
  },
  {
    id: 'aiml',
    domain: 'AI & Machine Learning',
    title: 'Artificial Intelligence & ML',
    icon: Brain,
    color: 'from-violet-500/20 to-indigo-600/10 text-violet-400 border-violet-500/30',
    description: 'Deep neural networks, Backpropagation, CNNs, Transformers, Gradient descent, and Loss functions.',
    example: 'How does backpropagation compute gradient descent in deep convolutional neural networks with ReLU?',
    prompt: 'How does backpropagation compute gradient descent in deep convolutional neural networks with ReLU and MaxPooling?'
  },
  {
    id: 'math',
    domain: 'Mathematics & Calculus',
    title: 'Mathematics & Calculus',
    icon: Calculator,
    color: 'from-emerald-500/20 to-teal-600/10 text-emerald-400 border-emerald-500/30',
    description: 'Symbolic derivatives, Definite integrals, Linear algebra, Matrix eigenvalues, and Limit theorems.',
    example: 'Find the symbolic derivative of f(x) = x^3 + 4*x^2 - 10 and calculate its critical points.',
    prompt: 'Find the symbolic derivative of f(x) = x^3 + 4*x^2 - 10 and calculate its critical points.'
  },
  {
    id: 'micro',
    domain: 'Electronics & Microcontrollers',
    title: 'Electronics & Microprocessors',
    icon: Cpu,
    color: 'from-amber-500/20 to-orange-600/10 text-amber-400 border-amber-500/30',
    description: 'Embedded 8051 timers, Harvard architecture, Logic gates, Semiconductor physics, and Interfacing.',
    example: 'Explain the Intel 8051 microcontroller architecture, Harvard memory organization, and timer mode 1.',
    prompt: 'Explain the Intel 8051 microcontroller architecture, Harvard memory organization, and how timer mode 1 functions.'
  },
  {
    id: 'physics',
    domain: 'Physics & Engineering',
    title: 'Physics & Engineering',
    icon: Atom,
    color: 'from-rose-500/20 to-pink-600/10 text-rose-400 border-rose-500/30',
    description: 'Quantum mechanics, Photoelectric effect, Thermodynamics, Electromagnetism, and Mechanics.',
    example: 'Explain the photoelectric effect, Einstein\'s photon hypothesis, and the work function equation.',
    prompt: 'Explain the photoelectric effect, Einstein\'s photon hypothesis, and the work function equation with physical significance.'
  },
  {
    id: 'dsa',
    domain: 'Algorithms & DS',
    title: 'Data Structures & Algorithms',
    icon: Code2,
    color: 'from-cyan-500/20 to-teal-600/10 text-cyan-400 border-cyan-500/30',
    description: 'Recursion, Time & Space Big-O complexity, Binary search trees, Dynamic programming, and Sorting.',
    example: 'How does recursion utilize the system call stack in Python? Write recursive binary search with complexity.',
    prompt: 'How does recursion utilize the system call stack in Python? Write a recursive binary search with base cases and time complexity.'
  }
];

export default function ChatTab({
  messages,
  setMessages,
  settings,
  stats,
  onRefreshStats,
  onOpenSettings
}) {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [attachedFile, setAttachedFile] = useState(null);

  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);
  const subjectCardsRef = useRef(null);

  // Auto-scroll on new message
  useEffect(() => {
    if (messages.length > 0) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  // Dynamic Learning Hours Calculation based on real metrics
  const totalDoubts = stats?.total_doubts || 0;
  const totalQuizzes = stats?.total_quizzes || 0;
  const totalCoding = stats?.total_coding || 0;
  const streak = stats?.study_streak || 0;
  const learningHours = (((totalDoubts * 8) + (totalQuizzes * 12) + (totalCoding * 15)) / 60).toFixed(1);
  const questionsPracticed = totalDoubts + totalQuizzes;

  const handleSendMessage = async (promptToSend) => {
    let text = promptToSend || inputText;
    if (attachedFile && attachedFile.content) {
      text = `${text}\n\n[Attached File: ${attachedFile.name}]\n${attachedFile.content}`;
    }

    if (!text || !text.trim() || loading) return;

    const userMsg = {
      role: 'user',
      content: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setAttachedFile(null);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: text.trim(),
          level: settings.level || 'Intermediate',
          mode: settings.mode || 'Step-by-step explanation',
          language: settings.language || 'English',
          attempt: settings.attempt || '',
          api_key: settings.apiKey || '',
          model: settings.provider || 'offline'
        })
      });

      if (!res.ok) {
        throw new Error(`Server returned HTTP ${res.status}`);
      }

      const data = await res.json();
      const assistantMsg = {
        role: 'assistant',
        content: data.answer,
        field: data.field || 'Universal Science',
        doubtId: data.doubt_id,
        questionRef: text.trim(),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        bookmarked: false,
        flaggedDifficult: false,
        liked: null
      };

      setMessages((prev) => [...prev, assistantMsg]);
      if (onRefreshStats) onRefreshStats();
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `❌ Could not complete request: ${err.message}. Please verify the backend connection.`,
          field: 'System Error',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = (questionRef) => {
    if (questionRef) {
      handleSendMessage(questionRef);
    }
  };

  const handleBookmark = async (idx, doubtId) => {
    if (!doubtId) return;
    try {
      const res = await fetch(`/api/history/bookmark/${doubtId}`, { method: 'POST' });
      const data = await res.json();
      setMessages((prev) =>
        prev.map((msg, i) => (i === idx ? { ...msg, bookmarked: data.bookmarked } : msg))
      );
    } catch (e) {
      console.error(e);
    }
  };

  const handleFlagDifficult = async (idx, doubtId) => {
    if (!doubtId) return;
    try {
      const res = await fetch(`/api/history/difficult/${doubtId}`, { method: 'POST' });
      const data = await res.json();
      setMessages((prev) =>
        prev.map((msg, i) => (i === idx ? { ...msg, flaggedDifficult: data.marked_difficult } : msg))
      );
    } catch (e) {
      console.error(e);
    }
  };

  const handleToggleLike = async (idx, doubtId, isLiked) => {
    setMessages((prev) =>
      prev.map((msg, i) =>
        i === idx ? { ...msg, liked: msg.liked === isLiked ? null : isLiked } : msg
      )
    );
    if (doubtId && isLiked) {
      try {
        await fetch(`/api/history/rate/${doubtId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ rating: 1 })
        });
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleCopy = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  const handleExportMarkdown = (msg) => {
    const md = `# DoubtBuster AI Academic Response\nDate: ${new Date().toLocaleString()}\nSubject: ${msg.field}\n\n---\n\n${msg.content}\n\n---\n*Verified by DoubtBuster 2.0 SymPy & AST Core Engine*`;
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `doubtbuster_answer_${Date.now()}.md`;
    link.click();
  };

  // Voice Input SpeechRecognition API
  const handleToggleVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Voice dictation is not supported in this browser. Please try Chrome or Edge.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      recognition.onerror = () => setIsListening(false);

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputText((prev) => (prev ? `${prev} ${transcript}` : transcript));
      };

      recognition.start();
    } catch (e) {
      console.error('Speech recognition error:', e);
      setIsListening(false);
    }
  };

  // File Attachment Handler
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      setAttachedFile({
        name: file.name,
        content: event.target.result.slice(0, 3000)
      });
    };
    reader.readAsText(file);
  };

  const scrollToSubjects = () => {
    subjectCardsRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-140px)] max-w-7xl mx-auto w-full">
      {/* Messages Feed View */}
      {messages.length > 0 ? (
        <div className="flex-1 space-y-6 pb-28">
          {/* Top Bar for active dialogue */}
          <div className="flex justify-between items-center py-2.5 px-3 rounded-xl bg-white/5 border border-white/5 text-xs">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span className="text-slate-300 font-medium">Academic Dialogue Active</span>
              <span className="text-slate-500">({messages.length} messages)</span>
            </div>
            <button
              onClick={() => setMessages([])}
              className="flex items-center gap-1.5 text-slate-400 hover:text-rose-400 transition-colors py-1 px-2.5 rounded-lg hover:bg-white/5"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Clear Dialogue</span>
            </button>
          </div>

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 md:gap-4 ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#7867FF]/25 to-[#22C8E5]/25 border border-[#7867FF]/40 flex items-center justify-center text-[#7867FF] shrink-0 mt-1 shadow-md">
                  <Sparkles className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-3xl rounded-2xl p-5 sm:p-6 shadow-xl ${
                  msg.role === 'user'
                    ? 'bg-[#161E36] border border-[#7867FF]/35 text-white ml-8'
                    : 'glass-card text-slate-200 mr-8'
                }`}
              >
                {/* Header of message */}
                <div className="flex items-center justify-between gap-3 mb-2.5 pb-2 border-b border-white/5">
                  <div className="flex items-center gap-2">
                    {msg.role === 'assistant' ? (
                      <>
                        <span className="text-xs font-bold text-white">DoubtBuster AI</span>
                        {msg.field && (
                          <span className="domain-badge text-[10px] py-0.5 px-2">
                            {msg.field}
                          </span>
                        )}
                      </>
                    ) : (
                      <span className="text-xs font-bold text-white flex items-center gap-1.5">
                        <User className="w-3.5 h-3.5 text-[#22C8E5]" /> Scholar Query
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono">{msg.timestamp}</span>
                </div>

                {/* Formatted Content */}
                <MathContent content={msg.content} />

                {/* Action Bar for Assistant Answers */}
                {msg.role === 'assistant' && (
                  <div className="flex flex-wrap items-center justify-between gap-2 pt-3 mt-4 border-t border-white/10 text-xs">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <button
                        onClick={() => handleBookmark(idx, msg.doubtId)}
                        className={`p-1.5 px-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-colors flex items-center gap-1 text-[11px] ${
                          msg.bookmarked ? 'border-amber-500/50 text-amber-400' : 'text-slate-300'
                        }`}
                        title="Bookmark to Study Notes"
                      >
                        <Bookmark className="w-3.5 h-3.5" />
                        <span className="hidden sm:inline">{msg.bookmarked ? 'Saved' : 'Bookmark'}</span>
                      </button>

                      <button
                        onClick={() => handleFlagDifficult(idx, msg.doubtId)}
                        className={`p-1.5 px-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-colors flex items-center gap-1 text-[11px] ${
                          msg.flaggedDifficult ? 'border-rose-500/50 text-rose-400' : 'text-slate-300'
                        }`}
                        title="Flag as Challenging Concept"
                      >
                        <Flag className="w-3.5 h-3.5" />
                        <span className="hidden sm:inline">{msg.flaggedDifficult ? 'Difficult' : 'Flag'}</span>
                      </button>

                      <button
                        onClick={() => handleRegenerate(msg.questionRef)}
                        className="p-1.5 px-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-colors flex items-center gap-1 text-[11px] text-slate-300 hover:text-white"
                        title="Regenerate Solution"
                      >
                        <RotateCcw className="w-3.5 h-3.5 text-[#22C8E5]" />
                        <span className="hidden sm:inline">Regenerate</span>
                      </button>

                      <button
                        onClick={() =>
                          handleSendMessage(
                            `Generate an interactive practice challenge with worked step-by-step solution based on this concept: ${
                              msg.questionRef ? msg.questionRef.slice(0, 100) : ''
                            }`
                          )
                        }
                        className="p-1.5 px-2 rounded-lg bg-[#7867FF]/10 border border-[#7867FF]/25 hover:bg-[#7867FF]/20 text-[#7867FF] transition-colors flex items-center gap-1 text-[11px] font-semibold"
                        title="Practice Similar Problem"
                      >
                        <Brain className="w-3.5 h-3.5" />
                        <span className="hidden sm:inline">Practice Problem</span>
                      </button>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={() => handleToggleLike(idx, msg.doubtId, true)}
                        className={`p-1.5 rounded-lg border transition-colors ${
                          msg.liked === true
                            ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-400'
                            : 'bg-white/5 border-white/10 text-slate-400 hover:text-white'
                        }`}
                        title="Helpful Answer"
                      >
                        <ThumbsUp className="w-3.5 h-3.5" />
                      </button>

                      <button
                        onClick={() => handleToggleLike(idx, msg.doubtId, false)}
                        className={`p-1.5 rounded-lg border transition-colors ${
                          msg.liked === false
                            ? 'bg-rose-500/20 border-rose-500/40 text-rose-400'
                            : 'bg-white/5 border-white/10 text-slate-400 hover:text-white'
                        }`}
                        title="Needs Improvement"
                      >
                        <ThumbsDown className="w-3.5 h-3.5" />
                      </button>

                      <button
                        onClick={() => handleExportMarkdown(msg)}
                        className="p-1.5 rounded-lg bg-white/5 border border-white/10 text-slate-400 hover:text-white transition-colors"
                        title="Export Markdown (.md)"
                      >
                        <Download className="w-3.5 h-3.5" />
                      </button>

                      <button
                        onClick={() => handleCopy(msg.content, idx)}
                        className="p-1.5 px-2 rounded-lg bg-white/5 border border-white/10 text-slate-300 hover:text-white transition-colors flex items-center gap-1 text-[11px]"
                        title="Copy Answer"
                      >
                        {copiedIdx === idx ? (
                          <>
                            <Check className="w-3.5 h-3.5 text-emerald-400" />
                            <span className="text-emerald-400">Copied</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3.5 h-3.5" />
                            <span>Copy</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#22C8E5]/30 to-[#7867FF]/30 border border-[#22C8E5]/40 flex items-center justify-center text-[#22C8E5] shrink-0 mt-1 shadow-md">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 md:gap-4 items-start animate-pulse">
              <div className="w-9 h-9 rounded-xl bg-[#7867FF]/20 border border-[#7867FF]/40 flex items-center justify-center text-[#7867FF] shrink-0 mt-1">
                <Sparkles className="w-4 h-4 animate-spin" />
              </div>
              <div className="glass-card p-5 max-w-xl text-xs text-slate-300 space-y-2.5">
                <div className="flex items-center gap-2 text-[#22C8E5] font-semibold">
                  <span className="w-2 h-2 rounded-full bg-[#22C8E5] animate-ping"></span>
                  <span>Synthesizing multi-domain academic derivation...</span>
                </div>
                <div className="h-2.5 bg-white/10 rounded-full w-3/4"></div>
                <div className="h-2.5 bg-white/5 rounded-full w-5/6"></div>
                <div className="h-2.5 bg-white/10 rounded-full w-2/3"></div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      ) : (
        /* Empty Landing Dashboard View */
        <div className="space-y-8 pb-32 animate-slide-up">
          {/* HERO BANNER */}
          <div className="hero-gradient p-6 sm:p-10 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 bg-[#7867FF]/15 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>
            <div className="absolute bottom-0 left-1/3 w-80 h-80 bg-[#22C8E5]/10 rounded-full blur-3xl pointer-events-none"></div>

            <div className="relative z-10 max-w-3xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-semibold text-[#22C8E5] mb-4 backdrop-blur-md">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                AI Engine Online • Multi-Domain Reasoning • SymPy & AST Verified
              </div>

              <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-3.5 leading-tight">
                Learn Smarter. Solve Faster.{' '}
                <span className="text-gradient">Master Everything.</span>
              </h2>

              <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6 max-w-2xl">
                Your personal AI academic companion for understanding concepts, solving complex problems and accelerating conceptual mastery with high mathematical precision.
              </p>

              <div className="flex flex-wrap items-center gap-3">
                <button
                  onClick={() => textareaRef.current?.focus()}
                  className="btn-primary"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>Ask AI Tutor</span>
                </button>
                <button
                  onClick={scrollToSubjects}
                  className="btn-secondary"
                >
                  <span>Explore Subjects</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          {/* DYNAMIC REAL STATISTICS CARDS */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="stat-card">
              <div className="stat-label flex items-center justify-between">
                <span>Total Doubts Solved</span>
                <CheckCircle2 className="w-4 h-4 text-[#22C8E5]" />
              </div>
              <div className="stat-value text-white">{totalDoubts}</div>
              <div className="text-[11px] text-[#94A3B8] font-medium">Logged in database</div>
            </div>

            <div className="stat-card">
              <div className="stat-label flex items-center justify-between">
                <span>Questions Asked</span>
                <HelpCircle className="w-4 h-4 text-[#7867FF]" />
              </div>
              <div className="stat-value text-white">{questionsPracticed}</div>
              <div className="text-[11px] text-[#94A3B8] font-medium">Doubts & practice questions</div>
            </div>

            <div className="stat-card">
              <div className="stat-label flex items-center justify-between">
                <span>Learning Hours</span>
                <Clock className="w-4 h-4 text-[#22C8E5]" />
              </div>
              <div className="stat-value text-white">{learningHours} <span className="text-sm font-normal text-slate-400">hrs</span></div>
              <div className="text-[11px] text-emerald-400 font-semibold">Active conceptual mastery</div>
            </div>

            <div className="stat-card">
              <div className="stat-label flex items-center justify-between">
                <span>Current Study Streak</span>
                <Flame className="w-4 h-4 text-amber-400 fill-amber-400" />
              </div>
              <div className="stat-value text-amber-400 flex items-center gap-1">
                {streak} <span className="text-sm font-normal text-slate-400">days</span>
              </div>
              <div className="text-[11px] text-[#94A3B8] font-medium">Consecutive learning activity</div>
            </div>
          </div>

          {/* SUBJECT EXPLORATION GRID */}
          <div ref={subjectCardsRef} className="pt-2 space-y-4">
            <div className="flex justify-between items-end">
              <div>
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <Brain className="w-5 h-5 text-[#7867FF]" />
                  Explore Academic Disciplines
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Select any foundational engineering or scientific domain to examine concepts or ask targeted doubts.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {SUBJECT_EXPLORATION_CARDS.map((card) => {
                const Icon = card.icon;
                return (
                  <div
                    key={card.id}
                    className="glass-card p-5 flex flex-col justify-between hover:border-[#7867FF]/50 hover:bg-[#161E36]/60 transition-all group cursor-pointer"
                    onClick={() => handleSendMessage(card.prompt)}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <div className={`p-2.5 rounded-xl bg-gradient-to-br ${card.color} border`}>
                          <Icon className="w-5 h-5" />
                        </div>
                        <span className="text-[11px] font-semibold text-slate-400 group-hover:text-white flex items-center gap-1 transition-colors">
                          Explore <ChevronRight className="w-3.5 h-3.5" />
                        </span>
                      </div>

                      <h4 className="text-base font-bold text-white group-hover:text-[#22C8E5] transition-colors mb-1.5">
                        {card.title}
                      </h4>

                      <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
                        {card.description}
                      </p>
                    </div>

                    <div className="pt-3 border-t border-white/5">
                      <div className="text-[10px] uppercase font-bold text-slate-500 mb-1">
                        Example Concept Query
                      </div>
                      <div className="text-xs text-slate-300 italic line-clamp-2">
                        "{card.example}"
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* FLOATING FROSTED GLASS COMPOSER DOCK */}
      <div className="fixed bottom-0 left-0 right-0 lg:left-68 p-4 bg-gradient-to-t from-[#070913] via-[#070913]/95 to-transparent z-30">
        <div className="max-w-4xl mx-auto space-y-2">
          {/* Attached File Preview Bar */}
          {attachedFile && (
            <div className="px-3.5 py-1.5 rounded-lg bg-[#161E36] border border-[#22C8E5]/30 flex items-center justify-between text-xs text-slate-200 animate-slide-up">
              <div className="flex items-center gap-2 truncate">
                <Paperclip className="w-3.5 h-3.5 text-[#22C8E5]" />
                <span className="font-semibold text-white truncate">{attachedFile.name}</span>
                <span className="text-slate-400 text-[11px]">(Attached for grounded reasoning)</span>
              </div>
              <button
                onClick={() => setAttachedFile(null)}
                className="text-slate-400 hover:text-rose-400 ml-2"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Composer Box */}
          <div className="relative rounded-2xl bg-[#0E1428] border border-white/15 focus-within:border-[#7867FF] focus-within:ring-2 focus-within:ring-[#7867FF]/20 transition-all shadow-2xl backdrop-blur-xl">
            <textarea
              ref={textareaRef}
              rows={2}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Ask DoubtBuster anything (e.g. solve calculus integral, explain 8086 queue, write recursive search)..."
              className="w-full bg-transparent border-0 resize-none text-white placeholder-slate-500 text-sm px-4 pt-3 pb-2 focus:ring-0 outline-none"
            />

            {/* Actions Inside Composer */}
            <div className="flex items-center justify-between px-3 pb-2.5 pt-1">
              <div className="flex items-center gap-1.5">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.py,.md,.pdf,.json"
                  onChange={handleFileUpload}
                  className="hidden"
                />

                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
                  title="Attach Document or Code Snippet"
                >
                  <Paperclip className="w-4 h-4" />
                </button>

                <button
                  type="button"
                  onClick={handleToggleVoice}
                  className={`p-1.5 rounded-lg transition-colors flex items-center gap-1 text-xs ${
                    isListening
                      ? 'bg-rose-500/20 text-rose-400 animate-pulse border border-rose-500/40'
                      : 'text-slate-400 hover:text-white hover:bg-white/5'
                  }`}
                  title={isListening ? 'Listening... click to stop' : 'Voice Input'}
                >
                  {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                  {isListening && <span className="text-[10px]">Listening...</span>}
                </button>

                {inputText.trim() && (
                  <button
                    type="button"
                    onClick={() => setInputText('')}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-white/5 transition-colors"
                    title="Clear Input"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleSendMessage()}
                  disabled={(!inputText.trim() && !attachedFile) || loading}
                  className="btn-primary py-1.5 px-4 text-xs font-semibold"
                >
                  <span>Ask Tutor</span>
                  <CornerDownLeft className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>

          {/* Footer Mode Indicator */}
          <div className="flex flex-wrap justify-between items-center text-[11px] text-slate-400 px-2">
            <div className="flex items-center gap-2">
              <span>Mode: <strong className="text-white">{settings.mode || 'Step-by-step'}</strong></span>
              <span>•</span>
              <span>Level: <strong className="text-[#22C8E5]">{settings.level || 'Intermediate'}</strong></span>
              <button
                onClick={onOpenSettings}
                className="text-[#7867FF] hover:underline ml-1 font-semibold flex items-center gap-1"
              >
                <Sliders className="w-3 h-3" /> Change
              </button>
            </div>
            <div className="hidden sm:flex items-center gap-1.5 text-slate-500">
              <span>Press <kbd className="px-1 py-0.5 rounded bg-white/5 text-slate-300 font-mono text-[10px]">Enter</kbd> to send, <kbd className="px-1 py-0.5 rounded bg-white/5 text-slate-300 font-mono text-[10px]">Shift+Enter</kbd> for newline</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
