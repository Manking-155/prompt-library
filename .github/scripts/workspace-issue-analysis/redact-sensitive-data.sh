#!/usr/bin/env bash
# Redact sensitive patterns from a text file before sending content to CLIs.
# Usage: redact-sensitive-data.sh <input-file> <output-file>
set -euo pipefail

INPUT_FILE="${1:-}"
OUTPUT_FILE="${2:-}"

if [[ -z "$INPUT_FILE" || -z "$OUTPUT_FILE" ]]; then
  echo "Usage: $0 <input-file> <output-file>" >&2
  exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input not found: $INPUT_FILE" >&2
  exit 1
fi

python3 - "$INPUT_FILE" "$OUTPUT_FILE" <<'PY'
import re
import sys

inp, outp = sys.argv[1], sys.argv[2]
text = open(inp, "r", encoding="utf-8", errors="replace").read()

# Order: more specific tokens first
patterns = [
    (r"github_pat_[A-Za-z0-9_]{20,}", "[REDACTED_GITHUB_PAT]"),
    (r"gho_[A-Za-z0-9]{36}", "[REDACTED_TOKEN]"),
    (r"ghu_[A-Za-z0-9]{36}", "[REDACTED_TOKEN]"),
    (r"ghs_[A-Za-z0-9]{36}", "[REDACTED_TOKEN]"),
    (r"ghr_[A-Za-z0-9]{36}", "[REDACTED_TOKEN]"),
    (r"ghp_[A-Za-z0-9]{36}", "[REDACTED_TOKEN]"),
    (r"\bAKIA[0-9A-Z]{16}\b", "[REDACTED_AWS_KEY]"),
    (r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", "[REDACTED_IP]"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[REDACTED_EMAIL]"),
    (r"(?i)\b([a-z0-9_-]*api[a-z0-9_-]*key|secret|token|password)\b\s*[:=]\s*(\S{12,})", r"\1: [REDACTED_SECRET]"),
    (r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "[REDACTED_UUID]"),
]

for pat, rep in patterns:
    text = re.sub(pat, rep, text)

open(outp, "w", encoding="utf-8").write(text)
PY
