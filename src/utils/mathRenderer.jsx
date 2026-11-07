import React from 'react';
import katex from 'katex';

/**
 * Safely parses text containing LaTeX expressions ($...$ for inline, $$...$$ for display)
 * and renders formatted HTML with KaTeX.
 */
export function renderFormattedMath(text) {
  if (!text) return '';

  try {
    // 1. Replace display math: $$...$$
    let formatted = text.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
      try {
        return katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false });
      } catch (e) {
        return `<pre class="text-rose-400 font-mono text-sm">${formula}</pre>`;
      }
    });

    // 2. Replace inline math: $...$ (avoiding currency signs followed by space or number)
    formatted = formatted.replace(/\$([^\$\n]+?)\$/g, (match, formula) => {
      try {
        return katex.renderToString(formula.trim(), { displayMode: false, throwOnError: false });
      } catch (e) {
        return `<code>${formula}</code>`;
      }
    });

    return formatted;
  } catch (err) {
    return text;
  }
}

export function MathContent({ content, className = '' }) {
  const html = renderFormattedMath(content);
  return (
    <div
      className={`prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

