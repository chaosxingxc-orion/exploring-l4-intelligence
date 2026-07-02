#!/usr/bin/env bash
# Build the W5 agent-level TFRL proposal PDF with TinyTeX.
# Pins a clean PATH to avoid the Windows-interop PATH mangling in WSL.
set -u
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:/usr/bin:/bin"
cd "$(dirname "$0")"

echo "=== pass 1: pdflatex ==="
pdflatex -interaction=nonstopmode -halt-on-error=0 main.tex > /tmp/tex1.log 2>&1
echo "=== bibtex ==="
bibtex main > /tmp/bibtex.log 2>&1
echo "=== pass 2: pdflatex ==="
pdflatex -interaction=nonstopmode main.tex > /tmp/tex2.log 2>&1
echo "=== pass 3: pdflatex ==="
pdflatex -interaction=nonstopmode main.tex > /tmp/tex3.log 2>&1

echo "=== RESULT ==="
ls -la main.pdf 2>/dev/null && echo "PDF_OK" || echo "PDF_MISSING"
echo "--- pages ---"
pdfinfo main.pdf 2>/dev/null | grep -i pages || true
echo "--- undefined citations (final pass) ---"
grep -c "Citation .* undefined" /tmp/tex3.log 2>/dev/null || echo 0
echo "--- undefined references (final pass) ---"
grep -c "Reference .* undefined\|There were undefined references" /tmp/tex3.log 2>/dev/null || echo 0
echo "--- fatal errors (pass1) ---"
grep -nE "^!|Fatal error|Emergency stop|Undefined control sequence|File .* not found" /tmp/tex1.log | head -40
