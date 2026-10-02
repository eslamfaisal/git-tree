#!/usr/bin/env bash
# Two unrelated tracked files modified and nothing staged: a new tag helper in src/tags.ts and a Tags section in the README.
set -euo pipefail
cat >> src/tags.ts <<'TS'

export function sortTags(tags: string[]): string[] {
  return [...tags].sort((a, b) => a.localeCompare(b));
}
TS
cat >> README.md <<'MD'

## Tags

    lumen tag add ideas "Reading list"
MD
