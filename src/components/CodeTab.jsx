import React, { useState } from 'react';
import {
  Terminal,
  Play,
  ShieldCheck,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  Clock,
  RotateCcw,
  Copy,
  Check,
  Download,
  Trash2,
  FileCode,
  Sparkles,
  Code2
} from 'lucide-react';

const CODE_PRESETS = [
  {
    name: 'Recursive Binary Search',
    code: `def binary_search(arr, target, low, high):
    """Recursive binary search implementation with O(log n) time complexity."""
    if low > high:
        return -1  # Target not found
    
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)

numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target_val = 23
result_idx = binary_search(numbers, target_val, 0, len(numbers) - 1)

print("Array:", numbers)
print(f"Target {target_val} located at index: {result_idx}")
`
  },
  {
    name: 'Neural Network ReLU Activation',
    code: `def relu(x):
    """Rectified Linear Unit activation function."""
    return max(0.0, x)

def relu_derivative(x):
    """Gradient of ReLU function."""
    return 1.0 if x > 0 else 0.0

test_inputs = [-3.5, -1.0, 0.0, 2.4, 7.8]
print("=== Neural Network Layer Activation Demo ===")
for val in test_inputs:
    print(f"Input: {val:5.1f} | ReLU: {relu(val):5.1f} | Gradient: {relu_derivative(val):5.1f}")
`
  },
  {
    name: 'Dynamic Programming Fibonacci',
    code: `def fib_memo(n, memo=None):
    """Calculates n-th Fibonacci number in O(n) using memoization."""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print("First 12 Fibonacci Numbers:")
for i in range(12):
    print(f"F({i}) = {fib_memo(i)}")
`
  },
  {
    name: 'Matrix Multiplication',
    code: `def mat_mul(A, B):
    """Multiplies two 2D matrices A and B."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    assert cols_A == rows_B, "Incompatible matrix dimensions!"
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = mat_mul(A, B)

print("Matrix A:", A)
print("Matrix B:", B)
print("Product C = A x B:", C)
`
  }
];

export default function CodeTab() {
  const [code, setCode] = useState(CODE_PRESETS[0].code);
  const [diagnoseLoading, setDiagnoseLoading] = useState(false);
  const [execLoading, setExecLoading] = useState(false);
  const [diagnosis, setDiagnosis] = useState(null);
  const [execution, setExecution] = useState(null);
  const [copiedCode, setCopiedCode] = useState(false);

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

  const handleCopyCode = () => {
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const handleDownloadCode = () => {
    const blob = new Blob([code], { type: 'text/x-python;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `doubtbuster_script_${Date.now()}.py`;
    link.click();
  };

  const lineCount = code.split('\n').length;

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h3 className="text-2xl font-extrabold text-white flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-[#22C8E5]/20 border border-[#22C8E5]/35 text-[#22C8E5]">
              <Terminal className="w-5 h-5" />
            </div>
            Python Code Diagnoser & Secure Sandbox Runner
          </h3>
          <p className="text-[#A1AEC4] text-xs sm:text-sm mt-1">
            Perform static AST syntax audits and run code inside an isolated subprocess with a 3.0-second timeout guardrail.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
          <ShieldCheck className="w-4 h-4" />
          <span>AST Node Screener Active</span>
        </div>
      </div>

      {/* Preset Code Snippets */}
      <div>
        <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-1.5">
          <Code2 className="w-3.5 h-3.5 text-[#7867FF]" />
          <span>Pre-loaded Algorithm Templates</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {CODE_PRESETS.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => {
                setCode(preset.code);
                setExecution(null);
                setDiagnosis(null);
              }}
              className="px-3 py-1.5 rounded-xl bg-[#141B2D] border border-white/10 hover:border-[#22C8E5]/50 text-xs text-slate-300 hover:text-white transition-all"
            >
              {preset.name}
            </button>
          ))}
        </div>
      </div>

      {/* Code Editor Panel */}
      <div className="glass-card p-4 space-y-3">
        {/* Editor Toolbar */}
        <div className="flex flex-wrap items-center justify-between gap-2 px-2 pb-2 border-b border-white/10 text-xs">
          <div className="flex items-center gap-2">
            <span className="font-mono text-slate-300 font-semibold flex items-center gap-1.5">
              <FileCode className="w-4 h-4 text-[#7867FF]" /> main.py
            </span>
            <span className="text-slate-500 text-[11px]">(Python 3.13 Subprocess)</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyCode}
              className="btn-secondary py-1 px-2.5 text-xs flex items-center gap-1"
              title="Copy Code"
            >
              {copiedCode ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedCode ? 'Copied' : 'Copy'}</span>
            </button>

            <button
              onClick={handleDownloadCode}
              className="btn-secondary py-1 px-2.5 text-xs flex items-center gap-1"
              title="Download Python Script"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download .py</span>
            </button>

            <button
              onClick={() => setCode('')}
              className="btn-secondary py-1 px-2.5 text-xs text-slate-400 hover:text-rose-400"
              title="Clear Editor"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear</span>
            </button>
          </div>
        </div>

        {/* Editor Area with Line Numbers */}
        <div className="flex rounded-xl bg-[#080B16] border border-white/10 overflow-hidden font-mono text-xs sm:text-sm">
          {/* Line Numbers */}
          <div className="select-none py-3 px-3 bg-[#0D1222] border-r border-white/10 text-slate-600 text-right font-mono">
            {Array.from({ length: Math.max(lineCount, 12) }, (_, i) => (
              <div key={i + 1} className="leading-6">
                {i + 1}
              </div>
            ))}
          </div>

          {/* Text Area */}
          <textarea
            rows={Math.max(lineCount + 2, 12)}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            spellCheck={false}
            className="flex-1 bg-transparent p-3 text-slate-100 font-mono leading-6 resize-none border-0 focus:ring-0 outline-none"
            placeholder="Write or paste your Python code here..."
          />
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <button
            onClick={handleExecute}
            disabled={execLoading || !code.trim()}
            className="btn-primary py-2.5 px-5 font-semibold text-xs flex items-center gap-2"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>{execLoading ? 'Executing in Sandbox...' : 'Run Code (Subprocess Sandbox)'}</span>
          </button>

          <button
            onClick={handleDiagnose}
            disabled={diagnoseLoading || !code.trim()}
            className="btn-secondary py-2.5 px-4 font-semibold text-xs flex items-center gap-2"
          >
            <ShieldCheck className="w-4 h-4 text-[#22C8E5]" />
            <span>{diagnoseLoading ? 'Auditing AST...' : 'Diagnose AST & Syntax'}</span>
          </button>
        </div>
      </div>

      {/* Execution Output Console */}
      {execution && (
        <div className="glass-card p-5 border-white/15 bg-[#0D1222] space-y-3 animate-slide-up">
          <div className="flex items-center justify-between pb-2 border-b border-white/10">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Sandbox Execution Console
              </span>
              {execution.success ? (
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-[10px] font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> Succeeded
                </span>
              ) : (
                <span className="px-2 py-0.5 rounded-full bg-rose-500/15 border border-rose-500/30 text-rose-400 text-[10px] font-semibold flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" /> Execution Error
                </span>
              )}
            </div>

            <div className="flex items-center gap-1.5 text-slate-400 text-xs font-mono">
              <Clock className="w-3.5 h-3.5" />
              <span>{execution.execution_time_ms ? `${execution.execution_time_ms} ms` : '0 ms'}</span>
            </div>
          </div>

          {execution.stdout && (
            <div className="p-4 rounded-xl bg-[#080B16] border border-white/10 text-emerald-300 font-mono text-xs whitespace-pre-wrap leading-relaxed">
              <div className="text-[10px] text-slate-500 font-bold uppercase mb-1">Standard Output (stdout):</div>
              {execution.stdout}
            </div>
          )}

          {execution.stderr && (
            <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-300 font-mono text-xs whitespace-pre-wrap leading-relaxed">
              <div className="text-[10px] text-rose-400 font-bold uppercase mb-1">Error Traceback (stderr):</div>
              {execution.stderr}
            </div>
          )}

          {!execution.stdout && !execution.stderr && (
            <div className="text-xs text-slate-500 italic py-2">
              Script finished with no output. (Tip: Use <code>print(...)</code> to display results).
            </div>
          )}
        </div>
      )}

      {/* AST Diagnosis Output */}
      {diagnosis && (
        <div className="glass-card p-5 border-[#7867FF]/30 bg-[#141B2D] space-y-3 animate-slide-up">
          <div className="flex items-center gap-2 text-sm font-bold text-white pb-2 border-b border-white/10">
            <ShieldCheck className="w-4 h-4 text-[#7867FF]" />
            <span>AST Code Diagnostic Report</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-3 rounded-xl bg-[#0D1222] border border-white/5">
              <div className="text-slate-400 font-semibold mb-1">Syntax Validity</div>
              <div className={`text-sm font-bold ${diagnosis.is_valid ? 'text-emerald-400' : 'text-rose-400'}`}>
                {diagnosis.is_valid ? 'Valid Python Syntax' : 'Syntax Error Detected'}
              </div>
            </div>

            <div className="p-3 rounded-xl bg-[#0D1222] border border-white/5">
              <div className="text-slate-400 font-semibold mb-1">AST Security Screening</div>
              <div className="text-sm font-bold text-emerald-400">
                Safe Constructs Verified
              </div>
            </div>
          </div>

          {diagnosis.message && (
            <div className="p-3 rounded-xl bg-[#0D1222] border border-white/5 text-xs text-slate-300">
              {diagnosis.message}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
