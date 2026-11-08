#!/usr/bin/env python3
"""Render submission/proposal.md to PoisonLens_Proposal.pdf (A4, Helvetica core fonts).

Pure stdlib — no third-party deps. Em-dash and middle-dot are WinAnsi-safe.
Usage: python3 scripts/build-proposal-pdf.py
"""
import re
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission" / "proposal.md"
OUT = ROOT / "submission" / "PoisonLens_Proposal.pdf"

PAGE_W, PAGE_H = 595.0, 842.0  # A4 portrait, points
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 56.0, 56.0, 64.0, 56.0
TEXT_W = PAGE_W - MARGIN_L - MARGIN_R

# Helvetica AFM widths (per 1000 units) for common chars; default 556.
W = {' ': 278, '!': 278, '"': 355, "'": 191, '(': 333, ')': 333, ',': 278,
     '-': 333, '.': 278, ':': 278, ';': 278, '?': 556, '`': 500, '·': 333,
     '—': 1000, '–': 556, '"': 333, '"': 500, '‘': 185, '’': 185,
     '/': 278, '@': 1015, '[': 278, ']': 278, '{': 334, '}': 334, '|': 260,
     '~': 584, '\u201c': 500, '\u201d': 500, '\u00b7': 333, '\u2014': 1000}
BOLD_EXTRA = 1.06  # bold glyphs are slightly wider; safety factor


def text_width(s, size, bold=False):
    total = 0
    for ch in s:
        base = W.get(ch, 556 if ch.isupper() else 500)
        total += base
    w = total / 1000.0 * size
    return w * BOLD_EXTRA if bold else w


def wrap(text, size, width, bold=False):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if text_width(cand, size, bold) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    out = []
    for ch in s:
        b = ch.encode('cp1252', errors='replace')
        c = b[0]
        if ch in '()\\':
            out.append('\\' + ch)
        elif 32 <= c < 127:
            out.append(chr(c))
        else:
            out.append('\\%03o' % c)
    return ''.join(out)


class Doc:
    def __init__(self):
        self.pages = []  # each: list of (font, size, x, y, text)
        self.cur = []
        self.y = PAGE_H - MARGIN_T

    def new_page(self):
        if self.cur:
            self.pages.append(self.cur)
        self.cur = []
        self.y = PAGE_H - MARGIN_T

    def line(self, font, size, text, x=MARGIN_L, lead=None):
        lead = lead or size * 1.38
        if self.y - lead < MARGIN_B:
            self.new_page()
        self.y -= lead
        self.cur.append((font, size, x, self.y, text))

    def space(self, pts):
        self.y -= pts
        if self.y < MARGIN_B:
            self.new_page()


def build():
    md = SRC.read_text(encoding='utf-8')
    doc = Doc()

    for raw in md.split('\n'):
        line = raw.rstrip()
        if not line.strip():
            doc.space(6.5)
            continue
        if line.startswith('# '):
            doc.space(4)
            for l in wrap(line[2:], 16, TEXT_W, bold=True):
                doc.line('/F2', 16, l)
            doc.space(2)
        elif line.startswith('## '):
            doc.space(9)
            doc.line('/F2', 11.5, esc(line[3:]))
            doc.space(1)
        elif line.startswith('**') and line.endswith('**'):
            doc.line('/F2', 10.5, esc(line.strip('*')))
            doc.space(3)
        elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            doc.space(4)
            for l in wrap(line.strip('*'), 9.5, TEXT_W):
                doc.line('/F3', 9.5, l)
        elif line.strip() == '---':
            doc.space(3)
            doc.line('/F1', 9.5, esc('-' * 52), lead=12)
            doc.space(2)
        else:
            for l in wrap(line, 10.5, TEXT_W):
                doc.line('/F1', 10.5, l)

    if doc.cur:
        doc.pages.append(doc.cur)

    # --- PDF assembly ---
    objs = {}
    n_pages = len(doc.pages)

    def add(num, body):
        objs[num] = body

    font_ids = {'/F1': 'Helvetica', '/F2': 'Helvetica-Bold', '/F3': 'Helvetica-Oblique'}
    fstart = 10
    for i, (k, name) in enumerate(font_ids.items()):
        add(fstart + i, f"<< /Type /Font /Subtype /Type1 /BaseFont /{name} /Encoding /WinAnsiEncoding >>")

    page_ids = []
    content_ids = []
    base = fstart + len(font_ids)
    for pi, page in enumerate(doc.pages):
        pid, cid = base + 2 * pi, base + 2 * pi + 1
        page_ids.append(pid)
        content_ids.append(cid)
        add(pid, (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W:.0f} {PAGE_H:.0f}] "
                  f"/Resources << /Font << /F1 {fstart} 0 R /F2 {fstart+1} 0 R /F3 {fstart+2} 0 R >> >> "
                  f"/Contents {cid} 0 R >>"))
        parts = ["BT"]
        for font, size, x, y, text in page:
            parts.append(f"{font} {size} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({text}) Tj")
        parts.append("ET")
        stream = '\n'.join(parts).encode('cp1252', errors='replace')
        comp = zlib.compress(stream)
        add(cid, (f"<< /Length {len(comp)} /Filter /FlateDecode >>\nstream\n").encode() + comp + b"\nendstream")

    kids = ' '.join(f"{p} 0 R" for p in page_ids)
    add(2, f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} >>")
    add(1, "<< /Type /Catalog /Pages 2 0 R >>")
    add(3, "<< /Title (PoisonLens - Round 1 Proposal) /Author (Rikh) /Producer (poisonlens build script) >>")

    max_id = max(objs)
    all_ids = sorted(objs)
    # Objects 4..9 unused placeholders keep numbering dense
    for gap in range(4, fstart):
        if gap not in objs:
            add(gap, "null")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    for num in sorted(objs):
        offsets[num] = len(out)
        body = objs[num]
        if isinstance(body, str):
            body = body.encode('cp1252', errors='replace')
        out += f"{num} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_pos = len(out)
    out += f"xref\n0 {max_id+1}\n".encode()
    out += b"0000000000 65535 f \n"
    for num in range(1, max_id + 1):
        if num in offsets:
            out += f"{offsets[num]:010d} 00000 n \n".encode()
        else:
            out += b"0000000000 65535 f \n"
    out += (f"trailer\n<< /Size {max_id+1} /Root 1 0 R /Info 3 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n").encode()

    OUT.write_bytes(bytes(out))
    print(f"wrote {OUT} ({len(out)} bytes, {n_pages} pages)")


if __name__ == '__main__':
    build()
