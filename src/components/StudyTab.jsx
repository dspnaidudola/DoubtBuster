import React, { useState, useEffect } from 'react';
import { BookOpen, FileText, Plus, Trash2, CheckCircle2, BookmarkCheck } from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

export default function StudyTab() {
  const [subTab, setSubTab] = useState('cheatsheets');
  const [materials, setMaterials] = useState({});
  const [selectedSubject, setSelectedSubject] = useState('Programming');

  // Notebook state
  const [notes, setNotes] = useState([]);
  const [noteTopic, setNoteTopic] = useState('');
  const [noteSubject, setNoteSubject] = useState('Programming');
  const [noteContent, setNoteContent] = useState('');
  const [showAddNote, setShowAddNote] = useState(false);

  useEffect(() => {
    fetchMaterials();
    fetchNotes();
  }, []);

  const fetchMaterials = async () => {
    try {
      const res = await fetch('/api/study/materials');
      const data = await res.json();
      setMaterials(data.materials || {});
    } catch (e) {
      console.error(e);
    }
  };

  const fetchNotes = async () => {
    try {
      const res = await fetch('/api/notes');
      const data = await res.json();
      setNotes(data.notes || []);
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreateNote = async (e) => {
    e.preventDefault();
    if (!noteTopic.trim() || !noteContent.trim()) return;

    try {
      await fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: noteSubject,
          topic: noteTopic.trim(),
          content: noteContent.trim()
        })
      });
      setNoteTopic('');
      setNoteContent('');
      setShowAddNote(false);
      fetchNotes();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteNote = async (id) => {
    try {
      await fetch(`/api/notes/${id}`, { method: 'DELETE' });
      setNotes((prev) => prev.filter((n) => n.id !== id));
    } catch (e) {
      console.error(e);
    }
  };

  const activeMaterial = materials[selectedSubject];

  return (
    <div className="space-y-6">
      {/* Sub Tab Switcher */}
      <div className="flex gap-2 p-1 bg-slate-900/80 border border-white/10 rounded-xl w-fit">
        <button
          onClick={() => setSubTab('cheatsheets')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'cheatsheets'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" /> Curated Subject Cheat Sheets
        </button>
        <button
          onClick={() => setSubTab('notebook')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'notebook'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <BookmarkCheck className="w-3.5 h-3.5" /> Student Revision Notebook
        </button>
      </div>

      {/* ========================================================= */}
      {/* SUB TAB 1: CURATED CHEAT SHEETS                           */}
      {/* ========================================================= */}
      {subTab === 'cheatsheets' && (
        <div className="space-y-6">
          <div className="glass-card p-6">
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Select Academic Subject Reference
            </label>
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full sm:w-80 text-xs"
            >
              {Object.keys(materials).map((s) => (
                <option key={s}>{s}</option>
              ))}
            </select>
          </div>

          {activeMaterial && (
            <div className="glass-card p-8 space-y-4">
              <div className="border-b border-white/10 pb-4">
                <h3 className="text-xl font-bold text-white mb-1">{activeMaterial.title}</h3>
                <p className="text-xs text-slate-400">{activeMaterial.description}</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/40 border border-white/5 text-xs text-slate-200">
                <MathContent content={activeMaterial.content} />
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* SUB TAB 2: REVISION NOTEBOOK                              */}
      {/* ========================================================= */}
      {subTab === 'notebook' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h4 className="text-sm font-bold text-white">Student Personal Revision Notebook</h4>
              <p className="text-xs text-slate-400">Save critical formulas, algorithms, and tutor takeaways to local SQLite.</p>
            </div>
            <button
              onClick={() => setShowAddNote(!showAddNote)}
              className="btn-primary py-2 px-4 text-xs font-semibold"
            >
              <Plus className="w-3.5 h-3.5" /> {showAddNote ? 'Close Form' : 'Add New Note'}
            </button>
          </div>

          {showAddNote && (
            <form onSubmit={handleCreateNote} className="glass-card p-6 space-y-4 border-indigo-500/40">
              <h4 className="text-sm font-bold text-white">➕ New Revision Note</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                    Topic / Concept
                  </label>
                  <input
                    type="text"
                    value={noteTopic}
                    onChange={(e) => setNoteTopic(e.target.value)}
                    placeholder="e.g. 8086 Memory Segmentation, Eigenvalues"
                    className="w-full text-xs"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                    Discipline
                  </label>
                  <select
                    value={noteSubject}
                    onChange={(e) => setNoteSubject(e.target.value)}
                    className="w-full text-xs"
                  >
                    <option>Programming</option>
                    <option>Mathematics</option>
                    <option>Machine Learning</option>
                    <option>Deep Learning</option>
                    <option>Microprocessors</option>
                    <option>Physics</option>
                    <option>Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Note Content / Formula / Code
                </label>
                <textarea
                  rows={4}
                  value={noteContent}
                  onChange={(e) => setNoteContent(e.target.value)}
                  placeholder="Type notes, formulas ($...$), or code..."
                  className="w-full text-xs"
                  required
                />
              </div>

              <button type="submit" className="btn-primary py-2 px-5 text-xs">
                Save Note to SQLite
              </button>
            </form>
          )}

          {/* Notes Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {notes.length === 0 ? (
              <div className="col-span-2 glass-card p-10 text-center text-slate-400 text-sm">
                No revision notes saved yet. Click <strong>Add New Note</strong> above to create your first study takeaway!
              </div>
            ) : (
              notes.map((n) => (
                <div key={n.id} className="glass-card p-5 space-y-3 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start gap-2 mb-2">
                      <div>
                        <span className="domain-badge text-[10px] py-0.5 px-2">🏷️ {n.subject}</span>
                        <h4 className="text-sm font-bold text-white mt-1">{n.topic}</h4>
                      </div>
                      <span className="text-[10px] text-slate-500">{n.created_at?.slice(0, 10)}</span>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-900/60 border border-white/5 text-xs text-slate-300">
                      <MathContent content={n.content} />
                    </div>
                  </div>

                  <div className="pt-2 border-t border-white/5 flex justify-end">
                    <button
                      onClick={() => handleDeleteNote(n.id)}
                      className="text-xs text-rose-400 hover:text-rose-300 flex items-center gap-1"
                    >
                      <Trash2 className="w-3 h-3" /> Delete Note
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
