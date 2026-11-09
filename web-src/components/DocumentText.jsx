'use client';

import { useEffect, useRef } from 'react';

/**
 * Renders the document's extracted text with the passages the audit quoted
 * marked up. The passages come from the recorded report, not from a live scan.
 */
export default function DocumentText({ text, parts, benign }) {
  const first = useRef(null);

  // The passage is often far down a long document — that is the point of it.
  // Bring it into view so the reader lands on what the audit found.
  useEffect(() => {
    const mark = first.current;
    if (!mark) return;
    // Scroll the document box only — never the page, or the reader loses the
    // banner explaining that these are recorded results.
    const box = mark.closest('.paper');
    if (!box) return;
    box.scrollTop = mark.offsetTop - box.clientHeight / 2 + mark.offsetHeight / 2;
  }, [text]);

  if (!parts || parts.length === 0) return <pre>{text}</pre>;

  // Walk the text once, slicing out each quoted fragment in the order it appears.
  const ordered = parts
    .map((p) => ({ p, at: text.indexOf(p) }))
    .filter((x) => x.at >= 0)
    .sort((a, b) => a.at - b.at);

  const nodes = [];
  let cursor = 0;
  ordered.forEach(({ p, at }, i) => {
    if (at < cursor) return;
    if (at > cursor) nodes.push(text.slice(cursor, at));
    nodes.push(
      <mark key={i} ref={i === 0 ? first : null} className={benign ? 'benign' : undefined}>
        {p}
      </mark>,
    );
    cursor = at + p.length;
  });
  if (cursor < text.length) nodes.push(text.slice(cursor));

  return <pre>{nodes}</pre>;
}
