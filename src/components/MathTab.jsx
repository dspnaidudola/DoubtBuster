import React, { useState } from 'react';
import { Calculator, Play, ChevronDown, ChevronRight, CheckCircle2, AlertCircle } from 'lucide-react';
import { MathContent } from '../utils/mathRenderer';

export default function MathTab() {
  const [mode, setMode] = useState('Solve Equation (f(x) = 0)');
  const [expression, setExpression] = useState('3*x + 12 = 33');
  const [variable, setVariable] = useState('x');
  const [matrixStr, setMatrixStr] = useState('1, 2; 3, 4');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSteps, setShowSteps] = useState(true);

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

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Calculator className="w-5 h-5 text-indigo-400" />
          Deterministic SymPy Mathematical Studio
        </h3>
        <p className="text-slate-400 text-xs md:text-sm mt-1">
          Verify calculus, algebraic equations, limits, and matrices with 100% mathematical precision and zero hallucinations.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls Column */}
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
              className="w-full"
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
                Matrix Format (e.g. <code>1, 2; 3, 4</code> or <code>[[1, 2], [3, 4]]</code>)
              </label>
              <textarea
                rows={3}
                value={matrixStr}
                onChange={(e) => setMatrixStr(e.target.value)}
                className="w-full font-mono text-sm"
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
                  className="w-full font-mono text-sm"
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
                  className="w-full font-mono text-sm text-center"
                />
              </div>
            </div>
          )}

          <button
            onClick={handleCompute}
            disabled={loading}
            className="btn-primary w-full py-2.5 mt-2"
          >
            <Play className="w-4 h-4 fill-white" />
            {loading ? 'Computing Symbolically...' : 'Compute Step-by-Step with SymPy'}
          </button>
        </div>

        {/* Syntax Helper Card */}
        <div className="lg:col-span-5 glass-card p-6 bg-slate-900/40">
          <h4 className="text-sm font-bold text-sky-400 mb-2">📝 Syntax Guide</h4>
          <p className="text-xs text-slate-400 mb-3">
            Write math expressions in natural or Python symbolic notation:
          </p>
          <ul className="text-xs text-slate-300 space-y-1.5 list-disc pl-4 font-mono">
            <li><strong>Equations:</strong> <code>3x + 12 = 33</code> or <code>x^2 - 9 = 0</code></li>
            <li><strong>Powers:</strong> <code>x^3</code> or <code>x**3</code></li>
            <li><strong>Multiplication:</strong> <code>2x</code> or <code>2*x</code>, <code>3(x+1)</code></li>
            <li><strong>Calculus:</strong> <code>sin(x)</code>, <code>exp(x)</code>, <code>log(x)</code></li>
            <li><strong>Matrices:</strong> <code>1, 2; 3, 4</code></li>
          </ul>
        </div>
      </div>

      {/* Result Display */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {result && result.type === 'math' && (
        <div className="glass-card p-6 border-indigo-500/40 bg-indigo-950/20 space-y-4">
          <div className="flex items-center gap-2 text-indigo-400 text-sm font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>{result.data.explanation}</span>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 text-center my-3">
            <MathContent content={`$$${result.data.latex_result}$$`} />
            <div className="text-xs text-slate-400 mt-2 font-mono">
              Raw result: <code>{result.data.result_str}</code>
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
                <div className="p-4 space-y-2 bg-slate-950/60 text-xs text-slate-300">
                  {result.data.steps.map((st, i) => (
                    <div key={i} className="flex gap-2 items-start py-1 border-b border-white/5 last:border-0">
                      <span className="text-indigo-400 font-bold">{i + 1}.</span>
                      <MathContent content={st} />
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {result && result.type === 'matrix' && (
        <div className="glass-card p-6 border-indigo-500/40 bg-indigo-950/20 space-y-4">
          <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Matrix Analyzed Successfully</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 text-center">
            <div className="text-xs text-slate-400 uppercase tracking-wider mb-2">Input Matrix $M$</div>
            <MathContent content={`$$M = ${result.data.latex_matrix}$$`} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="glass-card p-4 text-center">
              <div className="text-slate-400 mb-1">Dimensions</div>
              <div className="text-lg font-bold text-white">{result.data.rows} &times; {result.data.cols}</div>
            </div>
            <div className="glass-card p-4 text-center">
              <div className="text-slate-400 mb-1">Determinant \det(M)</div>
              <div className="text-lg font-bold text-sky-400"><MathContent content={`$$${result.data.determinant}$$`} /></div>
            </div>
            <div className="glass-card p-4 text-center">
              <div className="text-slate-400 mb-1">Invertible?</div>
              <div className="text-lg font-bold text-emerald-400">
                {result.data.is_invertible ? '✅ Yes (Non-Singular)' : '❌ No (Singular)'}
              </div>
            </div>
          </div>

          {result.data.is_invertible && result.data.latex_inverse && (
            <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 text-center">
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2">Inverse Matrix $M^{-1}$</div>
              <MathContent content={`$$M^{-1} = ${result.data.latex_inverse}$$`} />
            </div>
          )}

          {result.data.eigenvalues && (
            <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 text-xs">
              <span className="text-slate-400 font-semibold">Eigenvalues (Roots of Characteristic Equation): </span>
              <code className="text-indigo-300 font-mono">{result.data.eigenvalues}</code>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
