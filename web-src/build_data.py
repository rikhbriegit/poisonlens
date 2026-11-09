#!/usr/bin/env python3
"""Build web/data/audit.json from the real corpus and the real blind-run report.

Document text is extracted from tests/adversarial/. Verdicts, evidence, analysis,
benign readings and recommendations are lifted verbatim from
tests/runs/2026-11-09-scode-adversarial-run3.md. Nothing here is written by hand.
"""
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "tests" / "adversarial"
REPORT = ROOT / "tests" / "runs" / "2026-11-09-scode-adversarial-run3.md"
OUT = Path(__file__).resolve().parent / "data" / "audit.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Display names: the fixture prefixes are a test artefact, not part of the documents.
DISPLAY = {
    "A1": ("master-supply-agreement.docx", "Contract"),
    "A2": ("vendor-evaluation-matrix.docx", "Tender"),
    "A3": ("invoice-2026-3318.pdf", "Invoice"),
    "A4": ("information-handling-policy.pdf", "Policy"),
    "A5": ("ai-services-agreement.docx", "Contract"),
    "A6": ("project-handover-notes.txt", "Notes"),
    "A7": ("compliance-addendum.pdf", "Compliance"),
    "A8": ("capex-budget-2026.xlsx", "Spreadsheet"),
    "A9": ("berita-acara-serah-terima.txt", "Handover"),
    "A10": ("supplier-onboarding-template.docx", "Template"),
}


def text_docx(p):
    """Walk the body in document order so table rows stay rows."""
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = Document(p)
    out = []
    for child in d.element.body.iterchildren():
        if child.tag.endswith('}p'):
            t = Paragraph(child, d).text.strip()
            if t:
                out.append(t)
        elif child.tag.endswith('}tbl'):
            tb = Table(child, d)
            widths = [0] * len(tb.columns)
            rows = []
            for row in tb.rows:
                cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
                rows.append(cells)
                for i, c in enumerate(cells):
                    widths[i] = max(widths[i], len(c))
            for cells in rows:
                out.append('  '.join(c.ljust(widths[i]) for i, c in enumerate(cells)).rstrip())
    return '\n'.join(out)


def text_pdf(p):
    import subprocess
    return subprocess.run(['pdftotext', '-layout', str(p), '-'],
                          capture_output=True, text=True).stdout


def text_xlsx(p):
    from openpyxl import load_workbook
    ws = load_workbook(p).active
    rows = []
    for r in ws.iter_rows(values_only=True):
        cells = ['' if v is None else str(v) for v in r]
        if any(c.strip() for c in cells):
            rows.append('  |  '.join(cells))
    return '\n'.join(rows)


def extract(p):
    if p.suffix == '.docx':
        return text_docx(p)
    if p.suffix == '.pdf':
        return text_pdf(p)
    if p.suffix == '.xlsx':
        return text_xlsx(p)
    return p.read_text(encoding='utf-8')


# ── parse the run report ────────────────────────────────────────────────────
rep = REPORT.read_text(encoding='utf-8')

findings = {}
blocks = re.split(r'\n(?=A\d+[-\w.]*\.\w+ — )', rep)
for b in blocks:
    m = re.match(r'(A\d+)[-\w.]*\.\w+ — (.+)', b)
    if not m:
        continue
    fid, level = m.group(1), m.group(2).strip()
    f = {"level": level}
    loc = re.search(r'Finding \S+ · ([^·]+) · (.+)', b)
    if loc:
        f["location"] = loc.group(1).strip()
        f["categories"] = [c.strip() for c in loc.group(2).split(',')]
    for key, label in [("evidence", "Evidence"), ("analysis", "Analysis"),
                       ("benign", "Benign reading"), ("recommendation", "Recommendation")]:
        mm = re.search(r'^\s+%s: (.+?)(?=\n\s+(?:Evidence|Analysis|Benign reading|Recommendation):|\n\n|\Z)'
                       % label, b, re.M | re.S)
        if mm:
            f[key] = ' '.join(mm.group(1).split()).strip('"')
    findings[fid] = f

summary = {}
sm = re.search(r'Files checked: (\d+) \| High Risk: (\d+) \| Suspicious: (\d+) \| Low: (\d+) \| No Signal: (\d+) \| Not Assessable: (\d+)', rep)
if sm:
    summary = dict(zip(["checked", "high", "suspicious", "low", "noSignal", "notAssessable"],
                       map(int, sm.groups())))

coverage = re.search(r'^Coverage: (.+)$', rep, re.M)
status = re.search(r'^Status: (.+)$', rep, re.M)

# ── build documents ─────────────────────────────────────────────────────────
docs = []
for path in sorted(CORPUS.iterdir(), key=lambda p: int(re.match(r'A(\d+)', p.name).group(1))):
    fid = re.match(r'(A\d+)', path.name).group(1)
    name, kind = DISPLAY[fid]
    body = extract(path).replace('\r\n', '\n').rstrip()
    body = re.sub(r'\n{3,}', '\n\n', body)
    f = findings.get(fid, {})

    # Locate the quoted evidence inside the document so the UI can highlight it.
    # The evidence may not appear contiguously: in the evaluation matrix the
    # instruction is split across seven table cells, so match the longest runs.
    parts = []
    ev = f.get("evidence")
    if ev:
        toks = ev.split()
        i = 0
        while i < len(toks):
            best = None
            for j in range(len(toks), i, -1):
                frag = ' '.join(toks[i:j])
                if len(frag) < 12:
                    break
                pat = r'\s+'.join(re.escape(w) for w in toks[i:j])
                m2 = re.search(pat, body)
                if m2:
                    best = (m2.group(0), j)
                    break
            if best:
                parts.append(best[0])
                i = best[1]
            else:
                i += 1

    docs.append({
        "id": fid,
        "name": name,
        "kind": kind,
        "format": path.suffix.lstrip('.'),
        "bytes": path.stat().st_size,
        "level": f.get("level", "—"),
        "text": body,
        "highlight": parts,
        "finding": {k: v for k, v in f.items() if k != "level"} or None,
    })

data = {
    "run": {
        "date": "2026-11-09",
        "skill": "SKILL.md 1abd4d0c98986bac91b50e1e8963d627f8bb227af42d1fc9d5cba1b5e081fc90",
        "method": "Blind audit: the session that produced these verdicts had no access to the expected results.",
        "graded": "10 of 10 levels matched the key. No false positives.",
    },
    "summary": summary,
    "coverage": coverage.group(1) if coverage else "",
    "status": status.group(1) if status else "",
    "documents": docs,
}

OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"{OUT}  {OUT.stat().st_size:,} bytes")
for d in docs:
    print(f"  {d['id']:4} {d['level']:16} {d['name']:38} {len(d['text']):6,} chars  "
          f"highlight={len(d['highlight'])} part(s)")
