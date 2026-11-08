#!/usr/bin/env sh
# Build the uploadable PoisonLens skill package.
# Copies ONLY SKILL.md and references/ (the files the UGOS checker allows)
# into dist/poisonlens/, then zips it as dist/poisonlens.zip.
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
PKG="$DIST/poisonlens"

rm -rf "$PKG" "$DIST/poisonlens.zip"
mkdir -p "$PKG/references"

cp "$ROOT/SKILL.md" "$PKG/SKILL.md"
for f in "$ROOT"/references/*.md; do
  cp "$f" "$PKG/references/"
done

# zip: prefer Info-ZIP, fall back to python3 zipfile
if command -v zip >/dev/null 2>&1; then
  (cd "$DIST" && zip -r -X poisonlens.zip poisonlens)
else
  python3 - "$DIST" <<'EOF'
import os, sys, zipfile
dist = sys.argv[1]
out = os.path.join(dist, "poisonlens.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _, names in os.walk(os.path.join(dist, "poisonlens")):
        for n in sorted(names):
            full = os.path.join(base, n)
            z.write(full, os.path.relpath(full, dist))
print("wrote " + out)
EOF
fi

echo "Package contents:"
find "$PKG" -type f | sort
