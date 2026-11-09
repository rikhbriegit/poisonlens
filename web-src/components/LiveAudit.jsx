'use client';

import { useEffect, useState } from 'react';
import Chip from './Chip';

const MODELS = [
  { id: 'gpt-oss:20b-cloud', note: '20B — closest in size to a model running on the NAS' },
  { id: 'gemma4:31b-cloud', note: '31B — still device-plausible' },
  { id: 'deepseek-v4-flash:cloud', note: 'frontier scale, not a NAS proxy' },
  { id: 'glm-5.1:cloud', note: 'frontier scale, not a NAS proxy' },
];

export default function LiveAudit({ doc }) {
  const [model, setModel] = useState(MODELS[0].id);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // A result belongs to one document; clear it when the selection changes.
  useEffect(() => {
    setResult(null);
    setError(null);
  }, [doc.id]);

  async function run() {
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch('/api/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: doc.id, model }),
      });
      const data = await res.json();
      if (!res.ok) setError(data.error || `Request failed (${res.status}).`);
      else setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  const v = result?.verdict;
  const agrees = v && v.level === doc.level;

  return (
    <div className="live">
      <div className="live-head">
        <h3>Run it now</h3>
        <select value={model} onChange={(e) => setModel(e.target.value)} disabled={busy}>
          {MODELS.map((m) => (
            <option key={m.id} value={m.id}>
              {m.id}
            </option>
          ))}
        </select>
      </div>

      <button className={`run-btn ${result ? 'secondary' : ''}`} onClick={run} disabled={busy}>
        {busy ? 'Auditing…' : result ? 'Run again' : 'Audit this document'}
      </button>

      <p className="live-note">
        Sends this document and the submitted SKILL.md to Ollama Cloud and shows what comes
        back, right or wrong. {MODELS.find((m) => m.id === model)?.note}.
      </p>

      {error && <div className="err">{error}</div>}

      {v && (
        <div className="live-result">
          <div className="live-row">
            <Chip level={v.level} />
            <span>{result.model}</span>
            <span>{(result.ms / 1000).toFixed(1)}s</span>
            <span className={agrees ? 'agree' : 'differ'}>
              {agrees ? 'matches the recorded run' : `recorded run said ${result.recorded}`}
            </span>
          </div>

          {v.categories?.length > 0 && (
            <div className="cats" style={{ margin: '12px 0 0' }}>
              {v.categories.map((c) => (
                <span className="cat" key={c}>
                  {c}
                </span>
              ))}
            </div>
          )}

          {v.evidence && (
            <div className="live-field">
              <h5>Evidence</h5>
              <p style={{ fontFamily: 'var(--mono)', fontSize: 11.5 }}>&ldquo;{v.evidence}&rdquo;</p>
            </div>
          )}
          {v.analysis && (
            <div className="live-field">
              <h5>Analysis</h5>
              <p>{v.analysis}</p>
            </div>
          )}
          {v.benign && (
            <div className="live-field">
              <h5>Benign reading</h5>
              <p>{v.benign}</p>
            </div>
          )}
        </div>
      )}

      {result && !v && (
        <div className="err">
          The model did not return usable JSON. Raw reply:
          <div style={{ marginTop: 8, fontFamily: 'var(--mono)', fontSize: 11 }}>{result.raw}</div>
        </div>
      )}
    </div>
  );
}
