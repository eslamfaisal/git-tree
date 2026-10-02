#!/usr/bin/env bash
# One file, one hunk that mixes two ideas: a new size() method and, a few lines above it, tags added to the index.
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
p = Path('src/search/index.ts')
s = p.read_text()
s = s.replace('tokenize(`${note.title} ${note.body}`)', 'tokenize(`${note.title} ${note.body} ${note.tags.join(\' \')}`)', 1)
s = s.replace('  query(text: string): string[] {',
              '  /** How many distinct words are indexed. */\n  size(): number {\n    return this.postings.size;\n  }\n\n  query(text: string): string[] {', 1)
p.write_text(s)
PY
