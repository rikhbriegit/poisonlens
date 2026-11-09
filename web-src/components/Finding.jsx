import Chip from './Chip';

const BORDER = {
  'High Risk': { borderColor: 'var(--high)', background: 'var(--high-bg)', color: 'var(--high-ink)' },
  Suspicious: { borderColor: 'var(--susp)', background: 'var(--susp-bg)', color: 'var(--susp-ink)' },
  Low: { borderColor: 'var(--low)', background: 'var(--low-bg)', color: 'var(--low-ink)' },
  'No Signal': { borderColor: 'var(--none)', background: 'var(--none-bg)', color: 'var(--none-ink)' },
  'Not Assessable': { borderColor: 'var(--na)', background: 'var(--na-bg)', color: 'var(--na-ink)' },
};

export default function Finding({ doc }) {
  const f = doc.finding;
  const style = BORDER[doc.level] || BORDER['Not Assessable'];

  return (
    <>
      <div className="col-label">Verdict</div>

      <div className="verdict" style={style}>
        <div className="lvl">{doc.level}</div>
        {f?.location && <div className="loc">{f.location}</div>}
      </div>

      {!f && (
        <div className="clean">
          No text addressed to an AI was found in the analyzed content. That is not a
          clean bill of health: it means nothing was found in what could be read.
        </div>
      )}

      {f && (
        <>
          {f.categories && (
            <div className="cats">
              {f.categories.map((c) => (
                <span className="cat" key={c}>
                  {c}
                </span>
              ))}
            </div>
          )}

          {f.evidence && (
            <div className={`field quote ${doc.level === 'Low' ? 'low' : ''}`}>
              <h4>Evidence</h4>
              <p>&ldquo;{f.evidence}&rdquo;</p>
            </div>
          )}

          {f.analysis && (
            <div className="field">
              <h4>Analysis</h4>
              <p>{f.analysis}</p>
            </div>
          )}

          {f.benign && (
            <div className="field">
              <h4>Benign reading</h4>
              <p>{f.benign}</p>
            </div>
          )}

          {f.recommendation && (
            <div className="field">
              <h4>Recommendation</h4>
              <p>{f.recommendation}</p>
            </div>
          )}
        </>
      )}
    </>
  );
}
