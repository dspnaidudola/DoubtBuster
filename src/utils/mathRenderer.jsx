import React from 'react';
import katex from 'katex';

/**
 * Safely parses text containing Markdown + LaTeX expressions ($...$ inline, $$...$$ display)
 * and generates clean, styled HTML.
 */
export function renderFormattedMath(rawText) {
  if (!rawText) return '';

  try {
    let text = rawText;

    // 1. Process code blocks ```lang ... ```
    text = text.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      const escapedCode = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      return `<div class="my-3 rounded-xl bg-[#080B16] border border-white/10 overflow-hidden font-mono text-xs">
        <div class="flex justify-between items-center px-4 py-1.5 bg-[#0D1222] border-b border-white/10 text-slate-400 text-[11px]">
          <span>${lang || 'code'}</span>
          <span class="text-[10px] text-slate-500">Syntax Highlighted</span>
        </div>
        <pre class="p-4 text-emerald-300 overflow-x-auto leading-relaxed"><code>${escapedCode}</code></pre>
      </div>`;
    });

    // 2. Process inline code `...`
    text = text.replace(/`([^`\n]+)`/g, (match, code) => {
      const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<code class="px-1.5 py-0.5 rounded bg-white/10 font-mono text-xs text-[#22C8E5]">${escaped}</code>`;
    });

    // 3. Process display math: $$...$$
    text = text.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
      try {
        return katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false });
      } catch (e) {
        return `<pre class="text-rose-400 font-mono text-xs my-2">${formula}</pre>`;
      }
    });

    // 4. Process inline math: $...$
    text = text.replace(/\$([^\$\n]+?)\$/g, (match, formula) => {
      try {
        return katex.renderToString(formula.trim(), { displayMode: false, throwOnError: false });
      } catch (e) {
        return `<code class="text-sky-300">${formula}</code>`;
      }
    });

    // 5. Process Markdown Headings
    text = text.replace(/^### (.*$)/gim, '<h4 class="text-sm font-bold text-[#22C8E5] mt-4 mb-1.5 flex items-center gap-1.5">$1</h4>');
    text = text.replace(/^## (.*$)/gim, '<h3 class="text-base font-bold text-white mt-5 mb-2 pb-1 border-b border-white/10">$1</h3>');
    text = text.replace(/^# (.*$)/gim, '<h2 class="text-lg font-extrabold text-white mt-6 mb-2.5">$1</h2>');

    // 6. Process Bold and Italic
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-white">$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em class="text-slate-300">$1</em>');

    // 7. Process Lists
    text = text.replace(/^\s*[\-\*]\s+(.*$)/gim, '<li class="ml-4 list-disc text-slate-300 text-xs sm:text-sm my-0.5">$1</li>');
    text = text.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<li class="ml-4 list-decimal text-slate-300 text-xs sm:text-sm my-0.5">$2</li>');

    // 8. Line breaks (preserve double returns as paragraphs)
    text = text.replace(/\n\n/g, '<div class="h-2.5"></div>');

    return text;
  } catch (err) {
    return rawText;
  }
}

export function MathContent({ content, className = '' }) {
  const html = renderFormattedMath(content);
  return (
    <div
      className={`text-slate-200 text-sm leading-relaxed space-y-1 ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
