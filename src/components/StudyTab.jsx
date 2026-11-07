import React, { useState, useEffect, useRef } from 'react';
import {
  BookOpen,
  FileText,
  Plus,
  Trash2,
  CheckCircle2,
  BookmarkCheck,
  Search,
  UploadCloud,
  HelpCircle,
  Sparkles,
  Paperclip,
  X,
  Download,
  FileUp,
  Brain
} from 'lucide-react';
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
  const [noteSearch, setNoteSearch] = useState('');
  const [noteFilter, setNoteFilter] = useState('All');

  // Document QA & RAG State
  const [docFile, setDocFile] = useState(null);
  const [docText, setDocText] = useState('');
  const [ragQuery, setRagQuery] = useState('');
  const [ragLoading, setRagLoading] = useState(false);
  const [ragResponse, setRagResponse] = useState(null);

  const fileInputRef = useRef(null);

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

  // Document Upload for RAG
  const handleDocUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setDocFile(file);
    const reader = new FileReader();
    reader.onload = (event) => {
      setDocText(event.target.result);
      setRagResponse(null);
    };
    reader.readAsText(file);
  };

  // Submit Question on Document
  const handleAskDocument = async (customQuery) => {
    const q = customQuery || ragQuery;
    if (!q.trim() || !docText.trim() || ragLoading) return;

    setRagLoading(true);
    setRagResponse(null);

    try {
      const res = await fetch('/api/rag/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: q.trim(),
          document_text: docText,
          doc_name: docFile ? docFile.name : 'Uploaded Document'
        })
      });

      const data = await res.json();
      setRagResponse(data);
    } catch (err) {
      setRagResponse({ answer: `Failed to answer question on document: ${err.message}` });
    } finally {
      setRagLoading(false);
    }
  };

  const activeMaterial = materials[selectedSubject];

  const filteredNotes = notes.filter((n) => {
    const matchesSearch =
      n.topic.toLowerCase().includes(noteSearch.toLowerCase()) ||
      n.content.toLowerCase().includes(noteSearch.toLowerCase());
    const matchesFilter = noteFilter === 'All' || n.subject === noteFilter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full animate-slide-up">
      {/* Sub Tab Switcher */}
      <div className="flex flex-wrap gap-2 p-1 bg-[#0D1222] border border-white/10 rounded-xl w-fit">
        <button
          onClick={() => setSubTab('cheatsheets')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'cheatsheets'
              ? 'bg-[#7867FF] text-white shadow-lg shadow-[#7867FF]/30'
              : 'text-[#A1AEC4] hover:text-white'
          }`}
        >
          <BookOpen className="w-4 h-4" /> Curated Subject Cheat Sheets
        </button>
        <button
          onClick={() => setSubTab('notebook')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'notebook'
              ? 'bg-[#7867FF] text-white shadow-lg shadow-[#7867FF]/30'
              : 'text-[#A1AEC4] hover:text-white'
          }`}
        >
          <BookmarkCheck className="w-4 h-4" /> Personal Revision Notebook
        </button>
        <button
          onClick={() => setSubTab('rag')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'rag'
              ? 'bg-[#7867FF] text-white shadow-lg shadow-[#7867FF]/30'
              : 'text-[#A1AEC4] hover:text-white'
          }`}
        >
          <UploadCloud className="w-4 h-4" /> Document QA & RAG Assistant
        </button>
      </div>

      {/* ========================================================= */}
      {/* SUB TAB 1: CURATED CHEAT SHEETS                           */}
      {/* ========================================================= */}
      {subTab === 'cheatsheets' && (
        <div className="space-y-6">
          <div className="glass-card p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Select Academic Subject Reference
              </label>
              <select
                value={selectedSubject}
                onChange={(e) => setSelectedSubject(e.target.value)}
                className="w-full sm:w-80 text-xs bg-[#0D1222]"
              >
                {Object.keys(materials).map((s) => (
                  <option key={s}>{s}</option>
                ))}
              </select>
            </div>

            <div className="text-xs text-slate-400">
              Formulas & complexities verified with KaTeX rendering
            </div>
          </div>

          {activeMaterial && (
            <div className="glass-card p-6 sm:p-8 space-y-4">
              <div className="border-b border-white/10 pb-4">
                <h3 className="text-xl font-bold text-white mb-1">{activeMaterial.title}</h3>
                <p className="text-xs text-slate-400">{activeMaterial.description}</p>
              </div>

              <div className="p-5 rounded-2xl bg-[#080B16] border border-white/5 text-xs text-slate-200">
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
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h4 className="text-base font-bold text-white">Student Personal Revision Notebook</h4>
              <p className="text-xs text-slate-400">Save critical formulas, algorithms, and tutor takeaways to local SQLite.</p>
            </div>
            <button
              onClick={() => setShowAddNote(!showAddNote)}
              className="btn-primary py-2 px-4 text-xs font-semibold"
            >
              <Plus className="w-4 h-4" /> {showAddNote ? 'Close Form' : 'Add New Note'}
            </button>
          </div>

          {/* Search & Filter Bar */}
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                value={noteSearch}
                onChange={(e) => setNoteSearch(e.target.value)}
                placeholder="Search notes by topic or keyword..."
                className="w-full pl-9 text-xs bg-[#0D1222]"
              />
            </div>

            <select
              value={noteFilter}
              onChange={(e) => setNoteFilter(e.target.value)}
              className="sm:w-48 text-xs bg-[#0D1222]"
            >
              <option>All</option>
              <option>Programming</option>
              <option>Mathematics</option>
              <option>Machine Learning</option>
              <option>Deep Learning</option>
              <option>Microprocessors</option>
              <option>Physics</option>
            </select>
          </div>

          {showAddNote && (
            <form onSubmit={handleCreateNote} className="glass-card p-6 space-y-4 border-[#7867FF]/40 animate-slide-up">
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <Plus className="w-4 h-4 text-[#7867FF]" /> New Revision Note
              </h4>
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
                    className="w-full text-xs bg-[#0D1222]"
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
                    className="w-full text-xs bg-[#0D1222]"
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
                  placeholder="Type notes, formulas ($...$), or code snippets..."
                  className="w-full text-xs bg-[#0D1222]"
                  required
                />
              </div>

              <div className="flex justify-end">
                <button type="submit" className="btn-primary py-2 px-5 text-xs font-semibold">
                  Save Note to SQLite
                </button>
              </div>
            </form>
          )}

          {/* Notes Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredNotes.length === 0 ? (
              <div className="col-span-2 glass-card p-10 text-center text-slate-400 text-sm">
                No revision notes found. Click <strong>Add New Note</strong> above to create your first study takeaway!
              </div>
            ) : (
              filteredNotes.map((n) => (
                <div key={n.id} className="glass-card p-5 space-y-3 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start gap-2 mb-2">
                      <span className="domain-badge text-[10px] py-0.5 px-2">
                        {n.subject}
                      </span>
                      <button
                        onClick={() => handleDeleteNote(n.id)}
                        className="text-slate-500 hover:text-rose-400 transition-colors p-1"
                        title="Delete Note"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>

                    <h5 className="text-sm font-bold text-white mb-2">{n.topic}</h5>

                    <div className="text-xs text-slate-300 leading-relaxed max-h-40 overflow-y-auto">
                      <MathContent content={n.content} />
                    </div>
                  </div>

                  <div className="text-[10px] text-slate-500 pt-2 border-t border-white/5 font-mono">
                    Created: {n.created_at?.slice(0, 10)}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* SUB TAB 3: DOCUMENT QA & RAG ASSISTANT                   */}
      {/* ========================================================= */}
      {subTab === 'rag' && (
        <div className="space-y-6">
          <div className="glass-card p-6 space-y-4">
            <div>
              <h4 className="text-base font-bold text-white flex items-center gap-2">
                <UploadCloud className="w-5 h-5 text-[#22C8E5]" />
                Course Document & Notes QA with Grounded Citations
              </h4>
              <p className="text-xs text-slate-400 mt-1">
                Upload lecture notes, syllabi, or code files (.txt, .md, .py, .json) to ask targeted questions grounded in your course materials.
              </p>
            </div>

            {/* Hidden File Input */}
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,.md,.py,.json,.csv"
              onChange={handleDocUpload}
              className="hidden"
            />

            {/* Upload Area */}
            {!docFile ? (
              <div
                onClick={() => fileInputRef.current?.click()}
                className="p-8 border-2 border-dashed border-white/15 rounded-2xl hover:border-[#7867FF]/50 bg-[#0D1222]/60 hover:bg-[#141B2D] cursor-pointer text-center space-y-2 transition-all"
              >
                <div className="w-12 h-12 rounded-2xl bg-[#7867FF]/20 text-[#7867FF] mx-auto flex items-center justify-center">
                  <FileUp className="w-6 h-6" />
                </div>
                <div className="text-sm font-bold text-white">Click to Upload Course Material</div>
                <div className="text-xs text-slate-400">Supports text documents, Python scripts, Markdown notes (.txt, .md, .py)</div>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-[#0D1222] border border-white/10 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-[#22C8E5]/20 text-[#22C8E5]">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white">{docFile.name}</div>
                    <div className="text-[11px] text-slate-400 font-mono">
                      {(docFile.size / 1024).toFixed(1)} KB • Document text loaded
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      setDocFile(null);
                      setDocText('');
                      setRagResponse(null);
                    }}
                    className="btn-secondary py-1 px-2.5 text-xs text-slate-400 hover:text-rose-400"
                  >
                    <X className="w-3.5 h-3.5" /> Remove
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Quick Action Pills for Document */}
          {docText && (
            <div className="flex flex-wrap gap-2 animate-slide-up">
              <button
                onClick={() => handleAskDocument('Summarize the primary takeaways and main concepts of this document in structured bullet points.')}
                className="btn-secondary py-1.5 px-3 text-xs"
              >
                <Sparkles className="w-3.5 h-3.5 text-[#22C8E5]" /> Summarize Document
              </button>
              <button
                onClick={() => handleAskDocument('Extract all key formulas, algorithmic principles, and definition takeaways from this document.')}
                className="btn-secondary py-1.5 px-3 text-xs"
              >
                <Brain className="w-3.5 h-3.5 text-[#7867FF]" /> Extract Key Concepts
              </button>
              <button
                onClick={() => handleAskDocument('Generate 3 practice quiz questions with worked explanations based strictly on the material in this document.')}
                className="btn-secondary py-1.5 px-3 text-xs"
              >
                <BookOpen className="w-3.5 h-3.5 text-amber-400" /> Generate Practice Questions
              </button>
            </div>
          )}

          {/* QA Composer */}
          {docText && (
            <div className="glass-card p-6 space-y-4 animate-slide-up">
              <h5 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Ask a Question Grounded in Uploaded Material
              </h5>

              <div className="flex gap-2">
                <input
                  type="text"
                  value={ragQuery}
                  onChange={(e) => setRagQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleAskDocument();
                  }}
                  placeholder="Ask any question about this document..."
                  className="flex-1 text-xs bg-[#0D1222]"
                />
                <button
                  onClick={() => handleAskDocument()}
                  disabled={ragLoading || !ragQuery.trim()}
                  className="btn-primary py-2 px-5 text-xs font-semibold"
                >
                  <span>{ragLoading ? 'Retrieving Chunks...' : 'Ask Document'}</span>
                </button>
              </div>

              {/* RAG Answer Display */}
              {ragResponse && (
                <div className="p-5 rounded-2xl bg-[#080B16] border border-[#7867FF]/30 space-y-4 animate-slide-up">
                  <div className="flex items-center gap-2 text-[#22C8E5] text-xs font-bold uppercase tracking-wider">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Grounded RAG Tutor Solution</span>
                  </div>

                  <MathContent content={ragResponse.answer} />

                  {ragResponse.retrieved_chunks && ragResponse.retrieved_chunks.length > 0 && (
                    <div className="pt-3 border-t border-white/10 space-y-2">
                      <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        Retrieved Context Excerpts:
                      </div>
                      <div className="space-y-1.5">
                        {ragResponse.retrieved_chunks.map((chk, i) => (
                          <div key={i} className="p-2.5 rounded-lg bg-[#0D1222] border border-white/5 text-[11px] text-slate-400 leading-snug">
                            <span className="font-semibold text-slate-300">[{chk.doc_name} - {chk.section}]:</span> "{chk.content?.slice(0, 180)}..."
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
