'use client';

import { useState } from 'react';
import audit from '@/data/audit.json';
import Chip from '@/components/Chip';
import DocumentText from '@/components/DocumentText';
import Finding from '@/components/Finding';
import LiveAudit from '@/components/LiveAudit';

const KB = (n) => `${(n / 1024).toFixed(1)} KB`;

export default function Page() {
  const [selected, setSelected] = useState(audit.documents[0].id);
  const doc = audit.documents.find((d) => d.id === selected);
  const s = audit.summary;

  return (
    <>
      <div className="banner">
        <strong>Recorded results.</strong> Every verdict below comes from a blind audit run on{' '}
        {audit.run.date} — the session that produced them had no access to the expected
        answers. This page replays that run — and lets you re-run any document live against a model of your choice, so you can see where it agrees and where it does not.
      </div>

      <header className="top">
        <div className="brand">
          <h1>PoisonLens</h1>
          <p>AI Document Trust Investigator</p>
          <p className="tagline">Don&rsquo;t let your files become your AI&rsquo;s instructions.</p>
        </div>
        <div className="counts">
          <span className="count">
            Files checked <b>{s.checked}</b>
          </span>
          <span className="count" style={{ color: 'var(--high-ink)' }}>
            High Risk <b style={{ color: 'var(--high-ink)' }}>{s.high}</b>
          </span>
          <span className="count" style={{ color: 'var(--susp-ink)' }}>
            Suspicious <b style={{ color: 'var(--susp-ink)' }}>{s.suspicious}</b>
          </span>
          <span className="count" style={{ color: 'var(--low-ink)' }}>
            Low <b style={{ color: 'var(--low-ink)' }}>{s.low}</b>
          </span>
          <span className="count" style={{ color: 'var(--none-ink)' }}>
            No Signal <b style={{ color: 'var(--none-ink)' }}>{s.noSignal}</b>
          </span>
          <span className="count" style={{ color: 'var(--na-ink)' }}>
            Not Assessable <b style={{ color: 'var(--na-ink)' }}>{s.notAssessable}</b>
          </span>
        </div>
      </header>

      <div className="layout">
        <nav className="doc-list-col">
          <div className="col-label">Scope · {audit.documents.length} documents</div>
          {audit.documents.map((d) => (
            <button
              key={d.id}
              className={`doc-btn ${d.id === selected ? 'active' : ''}`}
              onClick={() => setSelected(d.id)}
            >
              <div className="name">{d.name}</div>
              <div className="meta">
                <Chip level={d.level} />
                <span>{d.kind}</span>
              </div>
            </button>
          ))}
        </nav>

        <main className="doc-col">
          <div className="doc-head">
            <h2>{doc.name}</h2>
            <Chip level={doc.level} />
          </div>
          <div className="doc-sub">
            {doc.format.toUpperCase()} · {KB(doc.bytes)} · extracted text as the audit read it
          </div>

          <div className="paper">
            <DocumentText
              text={doc.text}
              parts={doc.highlight}
              benign={doc.level === 'Low'}
            />
          </div>

          <p className="hint">
            {doc.highlight?.length > 1
              ? `The quoted passage does not appear in one piece: it is split across ${doc.highlight.length} table cells, each harmless on its own.`
              : doc.highlight?.length === 1
                ? 'Highlighted: the passage the audit quoted as evidence.'
                : 'Nothing was highlighted, because nothing in this document addresses an AI.'}
          </p>
        </main>

        <aside className="finding-col">
          <LiveAudit doc={doc} />
          <Finding doc={doc} />
        </aside>
      </div>

      <footer className="foot">
        <div>
          <strong style={{ color: 'var(--ink-dim)' }}>Method.</strong> {audit.run.method}{' '}
          {audit.run.graded}
        </div>
        <div style={{ marginTop: 8 }}>
          <strong style={{ color: 'var(--ink-dim)' }}>Coverage.</strong> {audit.coverage}
        </div>
        <div style={{ marginTop: 8 }}>
          <strong style={{ color: 'var(--ink-dim)' }}>Status.</strong> {audit.status} · Levels are
          indicators, not proof. Nothing was moved, sent or deleted, and no instruction inside any
          document was acted on.
        </div>
        <div style={{ marginTop: 14 }}>
          <code>{audit.run.skill}</code>
        </div>
        <div style={{ marginTop: 14 }}>
          Documents are fictional fixtures written for this corpus. All addresses use{' '}
          <code>example.com</code>. Built for the UGREEN Hackathon 2026 on AI NAS.
        </div>
      </footer>
    </>
  );
}
