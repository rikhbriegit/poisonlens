"""Validate PoisonLens against locally checkable Round 1 package constraints."""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist" / "poisonlens"
ZIP_PATH = ROOT / "dist" / "poisonlens.zip"


def fail(checks, name, detail):
    checks.append({"check": name, "pass": False, "detail": detail})


def ok(checks, name, detail):
    checks.append({"check": name, "pass": True, "detail": detail})


def main():
    checks = []
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        fail(checks, "SKILL.md exists", "missing")
        return emit(checks)
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        fail(checks, "frontmatter", "opening or closing delimiter missing")
    else:
        front = text[4:text.index("\n---\n", 4)]
        name = re.search(r"^name:\s*(\S+)\s*$", front, re.M)
        desc = re.search(r"^description:\s*(.+)$", front, re.M)
        if name and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)) and 2 <= len(name.group(1)) <= 64:
            ok(checks, "frontmatter.name", name.group(1))
        else:
            fail(checks, "frontmatter.name", "must be lowercase hyphenated, 2-64 chars")
        if desc and len(desc.group(1).strip()) <= 1024:
            ok(checks, "frontmatter.description", f"{len(desc.group(1).strip())} chars")
        else:
            fail(checks, "frontmatter.description", "missing or over 1024 chars")

    refs = ROOT / "references"
    linked = set(re.findall(r"(?:references/)?([A-Za-z0-9_.-]+\.md)", text))
    actual = {p.name for p in refs.glob("*.md")}
    missing = sorted(linked - actual)
    if missing:
        fail(checks, "reference links", f"missing: {missing}")
    else:
        ok(checks, "reference links", f"{len(actual)} reference files present; no missing linked file")

    if DIST.exists():
        files = [p for p in DIST.rglob("*") if p.is_file()]
        total = sum(p.stat().st_size for p in files)
        bad = [str(p.relative_to(DIST)) for p in files if p.stat().st_size > 1024 * 1024]
        if len(files) <= 100 and total <= 10 * 1024 * 1024 and not bad:
            ok(checks, "uncompressed package limits", f"{len(files)} files, {total} bytes")
        else:
            fail(checks, "uncompressed package limits", f"{len(files)} files, {total} bytes, oversized={bad}")
        names = {p.relative_to(DIST).as_posix() for p in files}
        expected = {"SKILL.md", *(f"references/{n}" for n in actual)}
        if names == expected:
            ok(checks, "package contents", ", ".join(sorted(names)))
        else:
            fail(checks, "package contents", f"expected={sorted(expected)}, actual={sorted(names)}")
    else:
        fail(checks, "uncompressed package exists", "dist/poisonlens missing")

    if ZIP_PATH.exists():
        size = ZIP_PATH.stat().st_size
        with zipfile.ZipFile(ZIP_PATH) as zf:
            names = {n.rstrip("/") for n in zf.namelist() if not n.endswith("/")}
            oversized = [n for n in names if zf.getinfo(n).file_size > 1024 * 1024]
        if size <= 10 * 1024 * 1024 and not oversized:
            ok(checks, "ZIP limits", f"{size} bytes")
        else:
            fail(checks, "ZIP limits", f"{size} bytes, oversized={oversized}")
        expected_zip = {f"poisonlens/{n}" for n in ("SKILL.md", *(f"references/{x}" for x in actual))}
        if names == expected_zip:
            ok(checks, "ZIP contents", ", ".join(sorted(names)))
        else:
            fail(checks, "ZIP contents", f"expected={sorted(expected_zip)}, actual={sorted(names)}")
    else:
        fail(checks, "ZIP exists", "dist/poisonlens.zip missing")

    proposal = ROOT / "submission" / "proposal.md"
    if proposal.exists():
        words = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", proposal.read_text(encoding="utf-8"))
        if len(words) <= 500:
            ok(checks, "proposal word limit", f"{len(words)} words")
        else:
            fail(checks, "proposal word limit", f"{len(words)} words")

    return emit(checks)


def emit(checks):
    result = {"validator": "local-round1-package-check", "official": False, "pass": all(c["pass"] for c in checks), "checks": checks}
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
