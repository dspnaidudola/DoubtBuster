import React, { useState, useEffect } from 'react';
import {
  Bookmark,
  Flag,
  Search,
  Trash2,
  Download,
  AlertCircle,
  Calendar,
  Tag,
  MessageSquare,
  Sparkles,
  ArrowRight,
  Filter
} from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

export default function HistoryTab({ onContinueInChat }) {
  const [historyItems, setHistoryItems] = useState([]);
  const [difficultTopics, setDifficultTopics] = useState([]);
  const [search, setSearch] = useState('');
  const [subjectFilter, setSubjectFilter] = useState('');
  const [bookmarkedOnly, setBookmarkedOnly] = useState(false);
  const [difficultOnly, setDifficultOnly] = useState(false);
  const [loading, setLoading] = useState(false);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, [subjectFilter, bookmarkedOnly, difficultOnly]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (subjectFilter) params.append('subject', subjectFilter);
      if (bookmarkedOnly) params.append('bookmarked_only', 'true');
      if (difficultOnly) params.append('difficult_only', 'true');
      if (search.trim()) params.append('search', search.trim());

      const res = await fetch(`/api/history?${params.toString()}`);
      const data = await res.json();
      setHistoryItems(data.items || []);
      setDifficultTopics(data.difficult_topics || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleBookmark = async (id) => {
    try {
      const res = await fetch(`/api/history/bookmark/${id}`, { method: 'POST' });
      const data = await res.json();
      setHistoryItems((prev) =>
        prev.map((item) => (item.id === id ? { ...item, bookmarked: data.bookmarked ? 1 : 0 } : item))
      );
    } catch (e) {
      console.error(e);
    }
  };

  const handleToggleDifficult = async (id) => {
    try {
      const res = await fetch(`/api/history/difficult/${id}`, { method: 'POST' });
      const data = await res.json();
      setHistoryItems((prev) =>
        prev.map((item) => (item.id === id ? { ...item, marked_difficult: data.marked_difficult ? 1 : 0 } : item))
      );
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteDoubt = async (id) => {
    try {
      await fetch(`/api/history/${id}`, { method: 'DELETE' });
      setHistoryItems((prev) => prev.filter((item) => item.id !== id));
      setConfirmDeleteId(null);
    } catch (e) {
      console.error(e);
    }
  };

  const handleExportMarkdown = () => {
    let md = `# DoubtBuster Student Learning History\nExported: ${new Date().toLocaleString()}\n\n`;
    historyItems.forEach((h, i) => {
      md += `## ${i + 1}. [${h.subject}] ${h.topic || 'General'}\n`;
      md += `**Date:** ${h.created_at?.slice(0, 10)} | **Status:** ${h.bookmarked ? '⭐ Bookmarked' : ''} ${h.marked_difficult ? '📌 Difficult' : ''}\n\n`;
      md += `### Question:\n${h.question}\n\n`;
      md += `### Guidance / Solution:\n${h.answer}\n\n---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `doubtbuster_history_${new Date().toISOString().slice(0, 10)}.md`;
    link.click();
  };

  const handleExportCSV = () => {
    const headers = ['id', 'subject', 'topic', 'question', 'bookmarked', 'marked_difficult', 'created_at'];
    let csv = headers.join(',') + '\n';
    historyItems.forEach((h) => {
      const row = [
        h.id,
        `"${(h.subject || '').replace(/"/g, '""')}"`,
        `"${(h.topic || '').replace(/"/g, '""')}"`,
        `"${(h.question || '').replace(/"/g, '""').slice(0, 150)}"`,
        h.bookmarked,
        h.marked_difficult,
        h.created_at
      ];
      csv += row.join(',') + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `doubtbuster_history_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full animate-slide-up">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h3 className="text-2xl font-extrabold text-white flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-[#7867FF]/20 border border-[#7867FF]/35 text-[#7867FF]">
              <Calendar className="w-5 h-5" />
            </div>
            Student Learning History & Revision Log
          </h3>
          <p className="text-[#A1AEC4] text-xs sm:text-sm mt-1">
            Browse previous academic queries, review mathematical derivations, and recall past tutor solutions.
          </p>
        </div>

        <div className="flex gap-2">
          <button onClick={handleExportMarkdown} className="btn-secondary py-1.5 px-3 text-xs flex items-center gap-1.5">
            <Download className="w-3.5 h-3.5" /> Export Markdown
          </button>
          <button onClick={handleExportCSV} className="btn-secondary py-1.5 px-3 text-xs flex items-center gap-1.5">
            <Download className="w-3.5 h-3.5" /> CSV
          </button>
        </div>
      </div>

      {/* Difficult Topics Revision Planner Card */}
      {difficultTopics.length > 0 && (
        <div className="glass-card p-6 border-amber-500/30 bg-amber-950/15">
          <h4 className="text-sm font-bold text-amber-400 flex items-center gap-2 mb-2">
            <AlertCircle className="w-4 h-4" />
            Personalized Revision Planner (Challenging Concepts)
          </h4>
          <p className="text-xs text-amber-200/80 mb-4">
            These concepts were flagged during your sessions. Prioritize revisiting them before upcoming tests:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
            {difficultTopics.slice(0, 4).map((dt, i) => (
              <div key={i} className="p-3.5 rounded-xl bg-[#080B16] border border-amber-500/25 text-xs">
                <div className="font-bold text-white mb-0.5">{dt.topic}</div>
                <div className="text-[11px] text-amber-300/80 mb-1">{dt.subject}</div>
                <div className="text-[10px] text-slate-400">Flagged {dt.count} times</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="glass-card p-5 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3.5 text-slate-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchHistory()}
              placeholder="Search past doubts..."
              className="w-full pl-9 text-xs bg-[#0D1222]"
            />
          </div>

          <div>
            <select
              value={subjectFilter}
              onChange={(e) => setSubjectFilter(e.target.value)}
              className="w-full text-xs bg-[#0D1222]"
            >
              <option value="">All Academic Disciplines</option>
              <option value="Computer Science & Programming">Computer Science & Programming</option>
              <option value="Mathematics & Statistics">Mathematics & Statistics</option>
              <option value="AI, Machine Learning & Data Science">AI, Machine Learning & Data Science</option>
              <option value="Computer Architecture & Microprocessors">Computer Architecture & Microprocessors</option>
              <option value="Electrical & Electronics Engineering">Electrical & Electronics Engineering</option>
              <option value="Physics & Physical Sciences">Physics & Physical Sciences</option>
              <option value="Economics, Business & Commerce">Economics, Business & Commerce</option>
            </select>
          </div>

          <div className="flex items-center gap-4 text-xs text-slate-300">
            <label className="flex items-center gap-1.5 cursor-pointer">
              <input
                type="checkbox"
                checked={bookmarkedOnly}
                onChange={(e) => setBookmarkedOnly(e.target.checked)}
                className="accent-[#7867FF]"
              />
              <span>⭐ Bookmarked</span>
            </label>

            <label className="flex items-center gap-1.5 cursor-pointer">
              <input
                type="checkbox"
                checked={difficultOnly}
                onChange={(e) => setDifficultOnly(e.target.checked)}
                className="accent-[#7867FF]"
              />
              <span>📌 Difficult</span>
            </label>
          </div>

          <div className="flex justify-end items-center text-xs text-slate-400">
            <span>Showing <strong className="text-white">{historyItems.length}</strong> records</span>
          </div>
        </div>
      </div>

      {/* History Items Feed */}
      <div className="space-y-4">
        {loading ? (
          <div className="text-center py-10 text-slate-500 text-sm">Loading learning history...</div>
        ) : historyItems.length === 0 ? (
          <div className="glass-card p-10 text-center text-slate-400 text-sm">
            No learning history found matching your filters. Ask a doubt in the AI Tutor tab to record your first study session!
          </div>
        ) : (
          historyItems.map((h) => (
            <div key={h.id} className="glass-card p-5 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="domain-badge">🏷️ {h.subject}</span>
                  {h.topic && <span className="text-slate-400 font-semibold">• {h.topic}</span>}
                </div>

                <div className="flex items-center gap-3 text-slate-400 text-[11px]">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" /> {h.created_at?.slice(0, 10)}
                  </span>
                  {h.bookmarked === 1 && <span className="text-amber-400 font-bold">⭐ Bookmarked</span>}
                  {h.marked_difficult === 1 && <span className="text-rose-400 font-bold">📌 Difficult</span>}
                </div>
              </div>

              <div className="text-sm font-bold text-white">
                ❓ {h.question}
              </div>

              <div className="p-4 rounded-xl bg-[#080B16] border border-white/5 text-xs text-slate-300">
                <MathContent content={h.answer} />
              </div>

              <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-white/5 text-xs">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleToggleBookmark(h.id)}
                    className={`btn-secondary py-1 px-2.5 text-xs ${
                      h.bookmarked ? 'border-amber-500/40 text-amber-400' : ''
                    }`}
                  >
                    <Bookmark className="w-3 h-3" /> {h.bookmarked ? 'Bookmarked' : 'Bookmark'}
                  </button>

                  <button
                    onClick={() => handleToggleDifficult(h.id)}
                    className={`btn-secondary py-1 px-2.5 text-xs ${
                      h.marked_difficult ? 'border-rose-500/40 text-rose-400' : ''
                    }`}
                  >
                    <Flag className="w-3 h-3" /> {h.marked_difficult ? 'Flagged' : 'Flag Difficult'}
                  </button>

                  {onContinueInChat && (
                    <button
                      onClick={() => onContinueInChat(h.question, h.answer)}
                      className="btn-secondary py-1 px-2.5 text-xs text-[#22C8E5] hover:text-white flex items-center gap-1"
                    >
                      <MessageSquare className="w-3 h-3" /> Continue in AI Tutor
                    </button>
                  )}
                </div>

                <div>
                  {confirmDeleteId === h.id ? (
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-rose-400">Delete this record?</span>
                      <button
                        onClick={() => handleDeleteDoubt(h.id)}
                        className="py-1 px-2 rounded bg-rose-600 text-white text-[11px] font-bold"
                      >
                        Yes
                      </button>
                      <button
                        onClick={() => setConfirmDeleteId(null)}
                        className="py-1 px-2 rounded bg-white/10 text-slate-300 text-[11px]"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => setConfirmDeleteId(h.id)}
                      className="btn-secondary py-1 px-2.5 text-xs text-slate-500 hover:text-rose-400"
                    >
                      <Trash2 className="w-3 h-3" /> Delete
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
