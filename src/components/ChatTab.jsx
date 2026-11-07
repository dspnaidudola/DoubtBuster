import React, { useState } from 'react';
import { Send, Bookmark, Flag, ThumbsUp, Brain, Copy, Check, Sparkles, User, CornerDownLeft } from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

const PROMPT_STARTERS = [
  {
    domain: "💻 Computer Architecture",
    title: "Intel 8086 Architecture",
    prompt: "Explain the Intel 8086 microprocessor internal architecture, detailing the difference between the BIU and EU, 6-byte instruction queue, and memory segmentation."
  },
  {
    domain: "🤖 AI & Machine Learning",
    title: "CNN & Backpropagation",
    prompt: "How does backpropagation compute gradient descent in deep convolutional neural networks with ReLU and MaxPooling?"
  },
  {
    domain: "🐍 Algorithms & DS",
    title: "Recursion & Call Stack",
    prompt: "How does recursion utilize the system call stack in Python? Write a recursive binary search with base cases and time complexity."
  },
  {
    domain: "📐 Mathematics & Calculus",
    title: "Symbolic Calculus Derivation",
    prompt: "Find the symbolic derivative of f(x) = x^3 + 4*x^2 - 10 and calculate its critical points."
  },
  {
    domain: "⚡ Electrical & Microcontrollers",
    title: "8051 Microcontroller & Timers",
    prompt: "Explain the Intel 8051 microcontroller architecture, Harvard memory organization, and how timer mode 1 functions."
  },
  {
    domain: "🔬 Physics & Engineering",
    title: "Photoelectric Effect & Photons",
    prompt: "Explain the photoelectric effect, Einstein's photon hypothesis, and the work function equation with physical significance."
  }
];

export default function ChatTab({
  messages,
  setMessages,
  settings,
  onRefreshStats
}) {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState(null);

  const handleSendMessage = async (promptToSend) => {
    const text = promptToSend || inputText;
    if (!text || !text.trim() || loading) return;

    const userMsg = {
      role: 'user',
      content: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
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
          model: settings.model || 'offline'
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
        rated: false
      };

      setMessages((prev) => [...prev, assistantMsg]);
      if (onRefreshStats) onRefreshStats();
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `❌ Could not complete request: ${err.message}. Please verify the backend connection or your API settings.`,
          field: 'Error System',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
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

  const handleRate = async (idx, doubtId) => {
    if (!doubtId) return;
    try {
      await fetch(`/api/history/rate/${doubtId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rating: 1 })
      });
      setMessages((prev) =>
        prev.map((msg, i) => (i === idx ? { ...msg, rated: true } : msg))
      );
    } catch (e) {
      console.error(e);
    }
  };

  const handleCopy = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-280px)] min-h-[550px]">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-6 pr-2">
        {messages.length === 0 ? (
          <div className="py-8">
            <div className="text-center max-w-2xl mx-auto mb-10">
              <h2 className="text-3xl font-extrabold text-gradient mb-3">
                Hello, Scholar 👋
              </h2>
              <p className="text-slate-400 text-sm md:text-base leading-relaxed">
                What would you like to master today? Ask doubts across <strong>Computer Science, Calculus, Microprocessors, AI/ML, Engineering, or Sciences</strong>. Every answer is synthesized dynamically with step-by-step logic, LaTeX math, and verified code.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
              {PROMPT_STARTERS.map((ps, i) => (
                <div
                  key={i}
                  onClick={() => handleSendMessage(ps.prompt)}
                  className="glass-card p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-white/5 transition-all group"
                >
                  <div className="text-xs font-semibold text-sky-400 mb-1">{ps.domain}</div>
                  <div className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors mb-2">
                    {ps.title}
                  </div>
                  <div className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                    {ps.prompt}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 md:gap-4 ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 shrink-0 mt-1">
                  <Sparkles className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-3xl rounded-2xl p-5 ${
                  msg.role === 'user'
                    ? 'bg-indigo-600/25 border border-indigo-500/35 text-white'
                    : 'glass-card text-slate-200'
                }`}
              >
                {msg.role === 'assistant' && msg.field && (
                  <div className="mb-3">
                    <span className="domain-badge">🏷️ {msg.field}</span>
                  </div>
                )}

                <MathContent content={msg.content} />

                {/* Assistant Action Bar */}
                {msg.role === 'assistant' && (
                  <div className="flex flex-wrap items-center gap-2 pt-4 mt-4 border-t border-white/10 text-xs">
                    <button
                      onClick={() => handleBookmark(idx, msg.doubtId)}
                      className={`btn-secondary py-1 px-2.5 text-xs ${
                        msg.bookmarked ? 'border-amber-500/50 text-amber-400' : ''
                      }`}
                    >
                      <Bookmark className="w-3.5 h-3.5" />
                      {msg.bookmarked ? 'Bookmarked' : 'Bookmark'}
                    </button>

                    <button
                      onClick={() => handleFlagDifficult(idx, msg.doubtId)}
                      className={`btn-secondary py-1 px-2.5 text-xs ${
                        msg.flaggedDifficult ? 'border-rose-500/50 text-rose-400' : ''
                      }`}
                    >
                      <Flag className="w-3.5 h-3.5" />
                      {msg.flaggedDifficult ? 'Flagged Difficult' : 'Flag Difficult'}
                    </button>

                    <button
                      onClick={() => handleRate(idx, msg.doubtId)}
                      disabled={msg.rated}
                      className={`btn-secondary py-1 px-2.5 text-xs ${
                        msg.rated ? 'text-emerald-400' : ''
                      }`}
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                      {msg.rated ? 'Rated Helpful' : 'Helpful'}
                    </button>

                    <button
                      onClick={() =>
                        handleSendMessage(
                          `Generate a similar practice problem with worked answer key based on this concept: ${
                            msg.questionRef ? msg.questionRef.slice(0, 100) : ''
                          }`
                        )
                      }
                      className="btn-secondary py-1 px-2.5 text-xs"
                    >
                      <Brain className="w-3.5 h-3.5 text-indigo-400" />
                      Practice Challenge
                    </button>

                    <button
                      onClick={() => handleCopy(msg.content, idx)}
                      className="btn-secondary py-1 px-2.5 text-xs ml-auto"
                    >
                      {copiedIdx === idx ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-400" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-sky-500/20 border border-sky-500/40 flex items-center justify-center text-sky-400 shrink-0 mt-1">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="flex gap-4 items-start">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 shrink-0">
              <Sparkles className="w-4 h-4 animate-spin" />
            </div>
            <div className="glass-card p-4 text-sm text-slate-400 flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-ping"></div>
              <span>Analyzing question & dynamically synthesizing domain explanation...</span>
            </div>
          </div>
        )}
      </div>

      {/* Floating Bottom Prompt Bar */}
      <div className="pt-4 border-t border-white/10 mt-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="relative flex items-center"
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask DoubtBuster anything across any domain (e.g. solve equation, write code, explain 8086 queue)..."
            className="w-full pr-24 pl-4 py-3.5 bg-slate-900/80 border border-white/15 rounded-xl text-white placeholder-slate-500 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 shadow-lg text-sm"
          />
          <button
            type="submit"
            disabled={!inputText.trim() || loading}
            className="absolute right-2 btn-primary py-2 px-4 text-xs font-semibold"
          >
            <span>Ask Tutor</span>
            <CornerDownLeft className="w-3.5 h-3.5" />
          </button>
        </form>
        <div className="flex justify-between items-center text-[11px] text-slate-500 px-1 pt-1.5">
          <span>Mode: <strong className="text-slate-400">{settings.mode || 'Step-by-step'}</strong> • Adaptive Level: <strong className="text-slate-400">{settings.level || 'Intermediate'}</strong></span>
          <span>Zero static answers • SymPy verified</span>
        </div>
      </div>
    </div>
  );
}

