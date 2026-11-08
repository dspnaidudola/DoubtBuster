import React, { useState } from 'react';
import {
  X,
  Sliders,
  Settings,
  Sparkles,
  Key,
  ShieldCheck,
  CheckCircle2,
  Globe,
  Brain,
  GraduationCap
} from 'lucide-react';

export default function SettingsModal({
  isOpen,
  onClose,
  settings,
  onUpdateSettings,
  adaptiveLevel
}) {
  if (!isOpen) return null;

  const [level, setLevel] = useState(settings.level || 'Intermediate');
  const [mode, setMode] = useState(settings.mode || 'Step-by-step explanation');
  const [language, setLanguage] = useState(settings.language || 'English');
  const [attempt, setAttempt] = useState(settings.attempt || '');
  const [provider, setProvider] = useState(settings.provider || 'offline');
  const [apiKey, setApiKey] = useState(settings.apiKey || '');
  const [showKey, setShowKey] = useState(false);

  const handleSave = () => {
    onUpdateSettings({
      level,
      mode,
      language,
      attempt,
      provider,
      apiKey
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-slide-up">
      <div className="glass-card w-full max-w-lg bg-[#0E1428] border-white/15 p-6 shadow-2xl space-y-5 rounded-2xl">
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-3 border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-[#7867FF]/20 text-[#7867FF]">
              <Sliders className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Tutor Pedagogical Controls</h3>
              <p className="text-[11px] text-slate-400">Personalize AI reasoning depth, pedagogical mode, and engine provider</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="space-y-4 max-h-[70vh] overflow-y-auto pr-1">
          {/* Skill Level */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                <GraduationCap className="w-4 h-4 text-[#22C8E5]" />
                Academic Skill Level
              </label>
              {adaptiveLevel && (
                <span className="text-[10px] font-semibold text-[#22C8E5] bg-[#22C8E5]/10 px-2 py-0.5 rounded-full border border-[#22C8E5]/25">
                  Calibrated: {adaptiveLevel}
                </span>
              )}
            </div>
            <select
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              className="w-full text-xs bg-[#161E36]"
            >
              <option value="Beginner">Beginner — Intuitive analogies & foundational concepts</option>
              <option value="Intermediate">Intermediate — Rigorous university-level derivations</option>
              <option value="Advanced">Advanced — Research-level formal proofs & algorithmic analysis</option>
            </select>
          </div>

          {/* Pedagogical Mode */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
              <Brain className="w-4 h-4 text-[#7867FF]" />
              Pedagogical Strategy
            </label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="w-full text-xs bg-[#161E36]"
            >
              <option value="Step-by-step explanation">Step-by-step complete explanation</option>
              <option value="Hint first">Socratic Hint First (Prompts your thinking)</option>
              <option value="Verify my answer">Verify my answer (Critique preliminary reasoning)</option>
              <option value="Practice question with answer key">Generate practice question with worked answer key</option>
            </select>
          </div>

          {mode === 'Verify my answer' && (
            <div className="p-3 rounded-xl bg-[#161E36] border border-white/10 space-y-1.5 animate-slide-up">
              <label className="block text-[11px] font-semibold text-slate-300">
                Your Preliminary Attempt / Reasoning
              </label>
              <textarea
                rows={3}
                value={attempt}
                onChange={(e) => setAttempt(e.target.value)}
                placeholder="Type your preliminary solution attempt here..."
                className="w-full text-xs bg-[#0B0F1D]"
              />
            </div>
          )}

          {/* Response Language */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
              <Globe className="w-4 h-4 text-emerald-400" />
              Response Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full text-xs bg-[#161E36]"
            >
              <option value="English">English (Standard Academic)</option>
              <option value="Simple English">Simple English (Clear, easy vocabulary)</option>
              <option value="Telugu (Technical mix)">Telugu (Technical engineering mix)</option>
              <option value="Hindi (Technical mix)">Hindi (Technical engineering mix)</option>
            </select>
          </div>

          {/* AI Provider & API Key */}
          <div className="pt-3 border-t border-white/10 space-y-3">
            <label className="block text-xs font-semibold text-slate-300 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Settings className="w-4 h-4 text-[#7867FF]" />
                AI Inference Engine
              </span>
              <span className="text-[10px] text-emerald-400 font-medium">SymPy Verification Always Active</span>
            </label>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="w-full text-xs bg-[#161E36]"
            >
              <option value="offline">Auto-detect / Free Built-in Offline Mode (Zero Cost)</option>
              <option value="gemini">Google Gemini 2.0 Flash / Pro</option>
              <option value="groq">Groq Llama-3.3-70B (Ultra Low Latency)</option>
              <option value="openai">OpenAI GPT-4o-mini</option>
            </select>

            {provider !== 'offline' && (
              <div className="space-y-1.5 animate-slide-up">
                <div className="flex justify-between items-center text-[11px] text-slate-400">
                  <span>{provider.toUpperCase()} API Key</span>
                  <button
                    type="button"
                    onClick={() => setShowKey(!showKey)}
                    className="text-[#22C8E5] hover:underline"
                  >
                    {showKey ? 'Hide' : 'Show'}
                  </button>
                </div>
                <input
                  type={showKey ? 'text' : 'password'}
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder={`Paste your ${provider} API Key...`}
                  className="w-full text-xs bg-[#161E36]"
                />
              </div>
            )}
          </div>
        </div>

        {/* Modal Footer */}
        <div className="flex justify-end gap-2 pt-3 border-t border-white/10">
          <button onClick={onClose} className="btn-secondary py-2 px-4 text-xs font-semibold">
            Cancel
          </button>
          <button onClick={handleSave} className="btn-primary py-2 px-5 text-xs font-semibold">
            Apply & Save
          </button>
        </div>
      </div>
    </div>
  );
}
