import React, { useState } from 'react';
import { Terminal, Play, ShieldAlert, CheckCircle2, AlertTriangle, Clock } from 'lucide-react';

const DEFAULT_CODE = `def calculate_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

print("Sum 1..10 is:", calculate_sum(10))
`;

export default function CodeTab() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [diagnoseLoading, setDiagnoseLoading] = useState(false);
  const [execLoading, setExecLoading] = useState(false);
  const [diagnosis, setDiagnosis] = useState(null);
  const [execution, setExecution] = useState(null);

  const handleDiagnose = async () => {
    setDiagnoseLoading(true);
    setDiagnosis(null);
    try {
      const res = await fetch('/api/code/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await res.json();
      setDiagnosis(data);
    } catch (err) {
      setDiagnosis({ success: false, error: err.message });
    } finally {
      setDiagnoseLoading(false);
    }
  };

  const handleExecute = async () => {
    setExecLoading(true);
    setExecution(null);
    try {
      const res = await fetch('/api/code/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, timeout_sec: 3.0 })
      });
      const data = await res.json();
      setExecution(data);
    } catch (err) {
      setExecution({
        success: false,
        stderr: err.message,
        execution_time_ms: 0
      });
    } finally {
      setExecLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Terminal className="w-5 h-5 text-indigo-400" />
          Python Code Diagnoser & Secure Sandbox Runner
        </h3>
        <p className="text-slate-400 text-xs md:text-sm mt-1">
          Perform static AST syntax audits and run code inside an isolated subprocess with a 3.0-second timeout guardrail.
        </p>
      </div>

      <div className="glass-card p-4 space-y-3">
        <div className="flex justify-between items-center text-xs text-slate-400 px-1">
          <span className="font-mono">main.py (Python 3.13)</span>
          <span className="flex items-center gap-1 text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" /> Subprocess Sandbox Active
          </span>
        </div>

        <textarea
          rows={10}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-full font-mono text-xs md:text-sm bg-slate-950/90 border-slate-800 text-emerald-300 p-4 leading-relaxed"
          spellCheck={false}
        />

        <div className="flex flex-wrap gap-3 pt-2">
          <button
            onClick={handleDiagnose}
            disabled={diagnoseLoading}
            className="btn-primary"
          >
            <ShieldAlert className="w-4 h-4" />
            {diagnoseLoading ? 'Auditing AST...' : 'Diagnose Code Statically'}
          </button>

          <button
            onClick={handleExecute}
            disabled={execLoading}
            className="btn-secondary"
          >
            <Play className="w-4 h-4 fill-white" />
            {execLoading ? 'Executing Sandbox...' : 'Run in Secure Sandbox'}
          </button>
        </div>
      </div>

      {/* Static Diagnosis Panel */}
      {diagnosis && (
        <div className="glass-card p-5 border-indigo-500/30 space-y-3">
          <h4 className="text-sm font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-indigo-400" />
            Static AST Analysis Results
          </h4>

          {diagnosis.is_clean ? (
            <div className="p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 shrink-0" />
              <span>Clean! Code passed all static syntax, security tokens, and AST checks.</span>
            </div>
          ) : (
            <div className="space-y-2">
              {!diagnosis.syntax_ok && (
                <div className="p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0" />
                  <span>Syntax Error: Code cannot be compiled by Python AST.</span>
                </div>
              )}
              {diagnosis.issues && diagnosis.issues.length > 0 && (
                <ul className="text-xs text-amber-300 space-y-1 list-disc pl-5">
                  {diagnosis.issues.map((iss, i) => (
                    <li key={i}>{iss}</li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      )}

      {/* Terminal Sandbox Execution Output */}
      {execution && (
        <div className="glass-card p-5 border-slate-700 bg-slate-950 space-y-3 font-mono">
          <div className="flex justify-between items-center text-xs pb-2 border-b border-white/10">
            <span className="flex items-center gap-2 text-slate-300">
              <Terminal className="w-4 h-4 text-sky-400" />
              <span>Execution Console Output</span>
            </span>
            <span className="flex items-center gap-1.5 text-slate-400 text-[11px]">
              <Clock className="w-3.5 h-3.5 text-amber-400" />
              <span>{execution.execution_time_ms} ms</span>
            </span>
          </div>

          {execution.success ? (
            <div className="text-emerald-400 text-xs whitespace-pre-wrap">
              {execution.stdout ? execution.stdout : '<Process exited with status 0 (no stdout)>'}
            </div>
          ) : (
            <div className="text-rose-400 text-xs whitespace-pre-wrap">
              {execution.stderr ? execution.stderr : 'Execution failed or timed out.'}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
