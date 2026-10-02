#!/usr/bin/env bash
# One file, two unrelated edits far apart (a doc comment and a result limit): two hunks to stage separately.
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
p = Path('src/search/index.ts')
s = p.read_text()
s = s.replace('export class SearchIndex {', '/** Inverted index: token -> ids of the notes that contain it. */\nexport class SearchIndex {', 1)
s = s.replace('  query(text: string): string[] {', '  query(text: string, limit = 20): string[] {', 1)
s = s.replace('    return [...sets[0]].filter((id) => sets.every((s) => s.has(id)));',
              '    const hits = [...sets[0]].filter((id) => sets.every((s) => s.has(id)));\n    return hits.slice(0, limit);', 1)
p.write_text(s)
PY
