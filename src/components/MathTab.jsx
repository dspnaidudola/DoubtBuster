import React, { useState } from 'react';
import {
  Calculator,
  Play,
  ChevronDown,
  ChevronRight,
  CheckCircle2,
  AlertCircle,
  Copy,
  Check,
  RotateCcw,
  Sparkles,
  BookOpen
} from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

const MATH_PRESETS = [
  {
    label: 'Quadratic Equation',
    mode: 'Solve Equation (f(x) = 0)',
    expr: 'x**2 - 5*x + 6 = 0',
    variable: 'x'
  },
  {
    label: 'Polynomial Derivative',
    mode: 'Symbolic Derivative',
    expr: 'x**3 + 4*x**2 - 10',
    variable: 'x'
  },
  {
    label: 'Integration by Parts',
    mode: 'Indefinite Integral',
    expr: 'x * exp(x)',
    variable: 'x'
  },
  {
    label: 'Trig Limit',
    mode: 'Limit (x \u2192 0)',
    expr: 'sin(x) / x',
    variable: 'x'
  },
  {
    label: 'Rational Simplification',
    mode: 'Simplify Expression',
    expr: '(x**2 - 1) / (x - 1)',
    variable: 'x'
  },
  {
    label: '2x2 Matrix Analysis',
    mode: 'Matrix Analysis',
    matrix: '1, 2; 3, 4'
  }
];

export default function MathTab() {
  const [mode, setMode] = useState('Solve Equation (f(x) = 0)');
  const [expression, setExpression] = useState('3*x + 12 = 33');
  const [variable, setVariable] = useState('x');
  const [matrixStr, setMatrixStr] = useState('1, 2; 3, 4');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSteps, setShowSteps] = useState(true);
  const [copiedLatex, setCopiedLatex] = useState(false);

  const handleApplyPreset = (preset) => {
    setMode(preset.mode);
    setResult(null);
    setError(null);
    if (preset.mode === 'Matrix Analysis') {
      setMatrixStr(preset.matrix);
    } else {
      setExpression(preset.expr);
      setVariable(preset.variable || 'x');
    }
  };

  const handleCompute = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      if (mode === 'Matrix Analysis') {
        const res = await fetch('/api/math/matrix', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ matrix_str: matrixStr })
        });
        const data = await res.json();
        if (data.success) {
          setResult({ type: 'matrix', data });
        } else {
          setError(data.error || 'Failed to compute matrix.');
        }
      } else {
        const opMap = {
          'Solve Equation (f(x) = 0)': 'solve',
          'Symbolic Derivative': 'derivative',
          'Indefinite Integral': 'integrate',
          'Simplify Expression': 'simplify',
          'Limit (x \u2192 0)': 'limit'
        };

        const res = await fetch('/api/math/solve', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            expression: expression.trim(),
            operation: opMap[mode] || 'solve',
            variable: variable.trim() || 'x'
          })
        });
        const data = await res.json();
        if (data.success) {
          setResult({ type: 'math', data });
        } else {
          setError(data.error || 'Computation failed.');
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyLatex = (latex) => {
    navigator.clipboard.writeText(latex);
    setCopiedLatex(true);
    setTimeout(() => setCopiedLatex(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h3 className="text-2xl font-extrabold text-white flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-[#7867FF]/20 border border-[#7867FF]/35 text-[#7867FF]">
              <Calculator className="w-5 h-5" />
            </div>
            Deterministic SymPy Math Studio
          </h3>
          <p className="text-[#A1AEC4] text-xs sm:text-sm mt-1">
            Perform high-precision symbolic calculus, algebraic equation solving, limits, and matrix decompositions with zero hallucinations.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
          <CheckCircle2 className="w-4 h-4" />
          <span>SymPy 1.12+ Engine Active</span>
        </div>
      </div>

      {/* Preset Problem Chips */}
      <div>
        <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-[#22C8E5]" />
          <span>Quick Preset Worksheets</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {MATH_PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleApplyPreset(p)}
              className="px-3 py-1.5 rounded-xl bg-[#141B2D] border border-white/10 hover:border-[#7867FF]/50 text-xs text-slate-300 hover:text-white transition-all"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Dual Workspace Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Input Panel */}
        <div className="lg:col-span-7 glass-card p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Select Mathematical Operation
            </label>
            <select
              value={mode}
              onChange={(e) => {
                setMode(e.target.value);
                setResult(null);
                setError(null);
              }}
              className="w-full bg-[#0D1222]"
            >
              <option>Solve Equation (f(x) = 0)</option>
              <option>Symbolic Derivative</option>
              <option>Indefinite Integral</option>
              <option>Simplify Expression</option>
              <option>Limit (x &#8594; 0)</option>
              <option>Matrix Analysis</option>
            </select>
          </div>

          {mode === 'Matrix Analysis' ? (
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Matrix Specification (Row-semicolon format: <code>1, 2; 3, 4</code>)
              </label>
              <textarea
                rows={3}
                value={matrixStr}
                onChange={(e) => setMatrixStr(e.target.value)}
                placeholder="1, 2; 3, 4"
                className="w-full font-mono text-sm bg-[#0D1222]"
              />
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
              <div className="sm:col-span-3">
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Mathematical Expression / Equation
                </label>
                <input
                  type="text"
                  value={expression}
                  onChange={(e) => setExpression(e.target.value)}
                  placeholder="e.g. 3*x + 12 = 33 or x**2 - 5*x + 6"
                  className="w-full font-mono text-sm bg-[#0D1222]"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Variable
                </label>
                <input
                  type="text"
                  value={variable}
                  onChange={(e) => setVariable(e.target.value)}
                  maxLength={2}
                  className="w-full font-mono text-sm text-center bg-[#0D1222]"
                />
              </div>
            </div>
          )}

          <button
            onClick={handleCompute}
            disabled={loading}
            className="btn-primary w-full py-3 mt-2 font-semibold text-sm"
          >
            <Play className="w-4 h-4 fill-white" />
            {loading ? 'Computing Symbolically...' : 'Compute Step-by-Step with SymPy'}
          </button>
        </div>

        {/* Syntax & Rules Helper Panel */}
        <div className="lg:col-span-5 glass-card p-6 bg-[#0D1222]/80 space-y-3">
          <h4 className="text-sm font-bold text-[#22C8E5] flex items-center gap-1.5">
            <BookOpen className="w-4 h-4" />
            <span>Mathematical Notation Guide</span>
          </h4>
          <p className="text-xs text-slate-400 leading-relaxed">
            Write mathematical equations using intuitive algebraic syntax or Python operators:
          </p>
          <ul className="text-xs text-slate-300 space-y-2 list-disc pl-4 font-mono">
            <li><strong>Equations:</strong> <code>3x + 12 = 33</code> or <code>x^2 - 9 = 0</code></li>
            <li><strong>Powers / Exponents:</strong> <code>x^3</code> or <code>x**3</code></li>
            <li><strong>Multiplication:</strong> <code>2x</code>, <code>2*x</code>, <code>3(x+1)</code></li>
            <li><strong>Trig & Logs:</strong> <code>sin(x)</code>, <code>exp(x)</code>, <code>log(x)</code></li>
            <li><strong>Matrices:</strong> <code>1, 2; 3, 4</code> (semicolon separates rows)</li>
          </ul>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Math Result Panel */}
      {result && result.type === 'math' && (
        <div className="glass-card p-6 border-[#7867FF]/40 bg-[#141B2D]/90 space-y-4 animate-slide-up">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-[#7867FF] text-sm font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>{result.data.explanation}</span>
            </div>
            <button
              onClick={() => handleCopyLatex(result.data.latex_result)}
              className="btn-secondary py-1 px-2.5 text-xs flex items-center gap-1"
            >
              {copiedLatex ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy LaTeX</span>
                </>
              )}
            </button>
          </div>

          <div className="p-6 rounded-2xl bg-[#080B16] border border-white/10 text-center my-3 shadow-inner">
            <div className="text-xs text-slate-400 font-mono mb-2">Exact Symbolic Solution:</div>
            <MathContent content={`$$${result.data.latex_result}$$`} />
            <div className="text-xs text-slate-500 mt-2 font-mono">
              Raw SymPy String: <code>{result.data.result_str}</code>
            </div>
          </div>

          {result.data.steps && result.data.steps.length > 0 && (
            <div className="border border-white/10 rounded-xl overflow-hidden mt-4">
              <button
                onClick={() => setShowSteps(!showSteps)}
                className="w-full p-3 bg-white/5 flex items-center justify-between text-xs font-bold text-slate-300 hover:bg-white/10 transition-colors"
              >
                <span>🔍 Step-by-Step Mathematical Derivation</span>
                {showSteps ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              </button>
              {showSteps && (
                <div className="p-4 space-y-2 bg-[#0D1222] text-xs text-slate-300">
                  {result.data.steps.map((st, i) => (
                    <div key={i} className="flex gap-2 items-start py-1.5 border-b border-white/5 last:border-0">
                      <span className="text-[#7867FF] font-bold">{i + 1}.</span>
                      <MathContent content={st} />
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Matrix Result Panel */}
      {result && result.type === 'matrix' && (
        <div className="glass-card p-6 border-[#22C8E5]/40 bg-[#141B2D]/90 space-y-4 animate-slide-up">
          <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Matrix Analyzed Symbolically</span>
          </div>

          <div className="p-5 rounded-2xl bg-[#080B16] border border-white/10 text-center">
            <div className="text-xs text-slate-400 uppercase tracking-wider mb-2 font-mono">Input Matrix $M$</div>
            <MathContent content={`$$M = ${result.data.latex_matrix}$$`} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="glass-card p-4 text-center bg-[#0D1222]">
              <div className="text-slate-400 mb-1 font-semibold uppercase text-[10px]">Dimensions</div>
              <div className="text-lg font-bold text-white">{result.data.rows} &times; {result.data.cols}</div>
            </div>
            <div className="glass-card p-4 text-center bg-[#0D1222]">
              <div className="text-slate-400 mb-1 font-semibold uppercase text-[10px]">Determinant \det(M)</div>
              <div className="text-lg font-bold text-[#22C8E5]"><MathContent content={`$$${result.data.determinant}$$`} /></div>
            </div>
            <div className="glass-card p-4 text-center bg-[#0D1222]">
              <div className="text-slate-400 mb-1 font-semibold uppercase text-[10px]">Invertible?</div>
              <div className="text-lg font-bold text-emerald-400">
                {result.data.is_invertible ? '✅ Yes (Non-Singular)' : '❌ No (Singular)'}
              </div>
            </div>
          </div>

          {result.data.is_invertible && result.data.latex_inverse && (
            <div className="p-5 rounded-2xl bg-[#080B16] border border-white/10 text-center">
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2 font-mono">Inverse Matrix $M^{-1}$</div>
              <MathContent content={`$$M^{-1} = ${result.data.latex_inverse}$$`} />
            </div>
          )}

          {result.data.eigenvalues && (
            <div className="p-4 rounded-xl bg-[#080B16] border border-white/10 text-xs">
              <span className="text-slate-400 font-semibold">Eigenvalues (Roots of Characteristic Equation): </span>
              <code className="text-[#22C8E5] font-mono">{result.data.eigenvalues}</code>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
