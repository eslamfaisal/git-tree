#!/usr/bin/env bash
# The shared history of the course's teaching repository ("lumen"). Copied from open-git-tree/scripts/demo/make-repo.sh
# without its uncommitted work: every episode starts from a named checkpoint (see build.sh) applied on top of this history.
#
# A fictional project ("lumen", a small Markdown notes tool) with ~40
# conventional commits by fictional authors, four feature branches, two
# --no-ff merges, a release tag, a bare "origin" so remote labels show, a
# branch that conflicts with main in exactly one hunk, a branch with fixup
# commits for interactive rebase, and nothing uncommitted: the clean tree.
# No real people, data or secrets.
#
# Usage: lumen-history.sh [dir]   (default /tmp/demo-repo); normally called by build.sh
# DEMO_EPOCH pins "now" (seconds) so a re-run is byte-identical; by default it
# is the current hour, so the app's relative dates read "2 days ago", not years.
set -euo pipefail

REPO=${1:-/tmp/demo-repo}
REMOTE="$REPO-origin.git"
NOW=${DEMO_EPOCH:-$(( $(date +%s) / 3600 * 3600 ))}
T=$(( NOW - 19 * 86400 ))   # history starts 19 days ago

rm -rf "$REPO" "$REMOTE"
git init -q -b main "$REPO"
git init -q --bare -b main "$REMOTE"
cd "$REPO"
git config user.name "Maya Chen"
git config user.email "maya.chen@example.com"
git config commit.gpgsign false
git config tag.gpgsign false
git config push.negotiate false   # the host may enable it; a local bare remote does not need it
git remote add origin "$REMOTE"

declare -A EMAIL=(
  ["Maya Chen"]=maya.chen@example.com
  ["Leo Okafor"]=leo.okafor@example.com
  ["Sara Lindqvist"]=sara.lindqvist@example.com
  ["Omar Haddad"]=omar.haddad@example.com
  ["Priya Nair"]=priya.nair@example.com
)

# commit AUTHOR MESSAGE — commits whatever is staged, advancing the clock by
# a few irregular hours so the graph's dates look like real work.
STEP=0
commit() {
  STEP=$(( STEP + 1 ))
  T=$(( T + 3600 * (3 + (STEP * 7) % 9) + 60 * ((STEP * 13) % 50) ))
  local d="@$T +0000"
  GIT_AUTHOR_NAME="$1" GIT_AUTHOR_EMAIL="${EMAIL[$1]}" GIT_AUTHOR_DATE="$d" \
  GIT_COMMITTER_NAME="$1" GIT_COMMITTER_EMAIL="${EMAIL[$1]}" GIT_COMMITTER_DATE="$d" \
    git commit -q --allow-empty-message -m "$2"
}
merge() { # merge AUTHOR BRANCH MESSAGE
  STEP=$(( STEP + 1 ))
  T=$(( T + 3600 * 2 ))
  local d="@$T +0000"
  GIT_AUTHOR_NAME="$1" GIT_AUTHOR_EMAIL="${EMAIL[$1]}" GIT_AUTHOR_DATE="$d" \
  GIT_COMMITTER_NAME="$1" GIT_COMMITTER_EMAIL="${EMAIL[$1]}" GIT_COMMITTER_DATE="$d" \
    git merge -q --no-ff "$2" -m "$3"
}
w() { mkdir -p "$(dirname "$1")"; cat > "$1"; git add "$1"; }  # write FILE from stdin, stage it
a() { cat >> "$1"; git add "$1"; }                              # append stdin to FILE, stage it

# ── main: scaffold ─────────────────────────────────────────────────────────
w README.md <<'EOF'
# lumen

Fast, local Markdown notes with full-text search.
EOF
w package.json <<'EOF'
{
  "name": "lumen",
  "version": "0.1.0",
  "type": "module",
  "scripts": { "build": "tsc", "test": "vitest run" }
}
EOF
commit "Maya Chen" "chore: initial project scaffold"

w tsconfig.json <<'EOF'
{ "compilerOptions": { "strict": true, "target": "ES2022", "module": "NodeNext", "outDir": "dist" } }
EOF
commit "Maya Chen" "build: add strict TypeScript config"

w src/note.ts <<'EOF'
export interface Note {
  id: string;
  title: string;
  body: string;
  tags: string[];
  updatedAt: Date;
}
EOF
commit "Leo Okafor" "feat(core): add Note model"

w src/store.ts <<'EOF'
import type { Note } from './note.js';

export class NoteStore {
  private readonly notes = new Map<string, Note>();

  save(note: Note): void {
    this.notes.set(note.id, { ...note, updatedAt: new Date() });
  }

  get(id: string): Note | undefined {
    return this.notes.get(id);
  }

  all(): Note[] {
    return [...this.notes.values()];
  }
}
EOF
commit "Leo Okafor" "feat(core): in-memory note store"

w src/config.ts <<'EOF'
export interface Config {
  notesDir: string;
  theme: 'light' | 'dark';
}

export function loadConfig(env: Record<string, string | undefined>): Config {
  return {
    notesDir: env.LUMEN_DIR ?? './notes',
    theme: 'light',
  };
}
EOF
commit "Sara Lindqvist" "feat(config): load settings from the environment"

w src/markdown.ts <<'EOF'
export function headings(markdown: string): string[] {
  return markdown
    .split('\n')
    .filter((line) => line.startsWith('#'))
    .map((line) => line.replace(/^#+\s*/, ''));
}
EOF
commit "Omar Haddad" "feat(markdown): extract headings"

w test/store.test.ts <<'EOF'
import { expect, test } from 'vitest';
import { NoteStore } from '../src/store.js';

test('saves and reads a note', () => {
  const store = new NoteStore();
  store.save({ id: 'a', title: 'A', body: '', tags: [], updatedAt: new Date(0) });
  expect(store.get('a')?.title).toBe('A');
});
EOF
commit "Priya Nair" "test(core): cover NoteStore save and get"

w .github/workflows/ci.yml <<'EOF'
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
EOF
commit "Maya Chen" "ci: run tests on every push"

a README.md <<'EOF'

## Install

    npm install -g lumen
EOF
commit "Maya Chen" "docs: installation instructions"
git push -q origin main

# ── feature/search ─────────────────────────────────────────────────────────
git checkout -q -b feature/search
w src/search/tokenize.ts <<'EOF'
export function tokenize(text: string): string[] {
  return text.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean);
}
EOF
commit "Omar Haddad" "feat(search): unicode-aware tokenizer"
w src/search/index.ts <<'EOF'
import type { Note } from '../note.js';
import { tokenize } from './tokenize.js';

export class SearchIndex {
  private readonly postings = new Map<string, Set<string>>();

  add(note: Note): void {
    for (const token of tokenize(`${note.title} ${note.body}`)) {
      const ids = this.postings.get(token) ?? new Set<string>();
      ids.add(note.id);
      this.postings.set(token, ids);
    }
  }

  query(text: string): string[] {
    const sets = tokenize(text).map((t) => this.postings.get(t) ?? new Set<string>());
    if (sets.length === 0) return [];
    return [...sets[0]].filter((id) => sets.every((s) => s.has(id)));
  }
}
EOF
commit "Omar Haddad" "feat(search): inverted index with AND queries"

git checkout -q main
w src/cli.ts <<'EOF'
#!/usr/bin/env node
import { loadConfig } from './config.js';

const config = loadConfig(process.env);
console.log(`lumen: notes in ${config.notesDir}`);
EOF
commit "Maya Chen" "feat(cli): entry point"

git checkout -q feature/search
w test/search.test.ts <<'EOF'
import { expect, test } from 'vitest';
import { SearchIndex } from '../src/search/index.js';

test('finds notes containing every word', () => {
  const index = new SearchIndex();
  index.add({ id: '1', title: 'Rust ownership', body: 'borrowing rules', tags: [], updatedAt: new Date(0) });
  index.add({ id: '2', title: 'Go channels', body: 'ownership of goroutines', tags: [], updatedAt: new Date(0) });
  expect(index.query('ownership rules')).toEqual(['1']);
});
EOF
commit "Priya Nair" "test(search): AND query semantics"
a src/search/tokenize.ts <<'EOF'

export const STOP_WORDS = new Set(['a', 'an', 'the', 'of', 'and']);
EOF
commit "Omar Haddad" "perf(search): skip stop words while indexing"
git push -q origin feature/search

git checkout -q main
merge "Maya Chen" feature/search "Merge branch 'feature/search'"

# ── feature/dark-mode ──────────────────────────────────────────────────────
git checkout -q -b feature/dark-mode
w src/theme.ts <<'EOF'
export const palettes = {
  light: { background: '#ffffff', text: '#1f2328' },
  dark: { background: '#0d1117', text: '#e6edf3' },
} as const;
EOF
commit "Sara Lindqvist" "feat(theme): light and dark palettes"

git checkout -q main
w src/tags.ts <<'EOF'
export function normalizeTag(tag: string): string {
  return tag.trim().toLowerCase().replace(/\s+/g, '-');
}
EOF
commit "Leo Okafor" "feat(core): normalize tags"

git checkout -q feature/dark-mode
a src/theme.ts <<'EOF'

export function prefersDark(media: { matches: boolean }): boolean {
  return media.matches;
}
EOF
commit "Sara Lindqvist" "feat(theme): follow the system colour scheme"

git checkout -q main
a src/markdown.ts <<'EOF'

export function wordCount(markdown: string): number {
  return markdown.split(/\s+/).filter(Boolean).length;
}
EOF
commit "Omar Haddad" "feat(markdown): word count"

git checkout -q feature/dark-mode
w test/theme.test.ts <<'EOF'
import { expect, test } from 'vitest';
import { prefersDark } from '../src/theme.js';

test('follows the system preference', () => {
  expect(prefersDark({ matches: true })).toBe(true);
});
EOF
commit "Priya Nair" "test(theme): system preference"
git push -q origin feature/dark-mode

git checkout -q main
w test/markdown.test.ts <<'EOF'
import { expect, test } from 'vitest';
import { headings } from '../src/markdown.js';

test('extracts headings', () => {
  expect(headings('# One\ntext\n## Two')).toEqual(['One', 'Two']);
});
EOF
commit "Priya Nair" "test(markdown): headings"
merge "Sara Lindqvist" feature/dark-mode "Merge branch 'feature/dark-mode'"

a README.md <<'EOF'

## Search

    lumen search "ownership rules"
EOF
commit "Maya Chen" "docs: document search"
sed -i 's/"version": "0.1.0"/"version": "1.0.0"/' package.json; git add package.json
commit "Maya Chen" "chore(release): 1.0.0"
GIT_COMMITTER_DATE="@$T +0000" GIT_COMMITTER_NAME="Maya Chen" GIT_COMMITTER_EMAIL="${EMAIL["Maya Chen"]}" \
  git tag -a v1.0.0 -m "lumen 1.0.0"
git push -q origin main v1.0.0

# ── after the release ──────────────────────────────────────────────────────
BASE_FOR_FIX=$(git rev-parse HEAD)
w src/sync.ts <<'EOF'
export interface SyncTarget {
  url: string;
  intervalMinutes: number;
}
EOF
commit "Leo Okafor" "feat(sync): sync target model"
a src/store.ts <<'EOF'

export function byUpdated(a: Note, b: Note): number {
  return b.updatedAt.getTime() - a.updatedAt.getTime();
}
EOF
commit "Leo Okafor" "feat(core): sort notes by last update"
# main's side of the conflict: the theme now comes from the environment.
sed -i "s/    theme: 'light',/    theme: env.LUMEN_THEME === 'dark' ? 'dark' : 'light',/" src/config.ts; git add src/config.ts
commit "Sara Lindqvist" "feat(config): read the theme from LUMEN_THEME"
a src/markdown.ts <<'EOF'

export function excerpt(markdown: string, length = 140): string {
  return markdown.replace(/[#*_`>]/g, '').slice(0, length);
}
EOF
commit "Omar Haddad" "feat(markdown): plain-text excerpts"
git push -q origin main

# ── fix/config-defaults: conflicts with main in src/config.ts, one hunk ────
git checkout -q -b fix/config-defaults "$BASE_FOR_FIX"
sed -i "s/    theme: 'light',/    theme: env.LUMEN_THEME === 'light' ? 'light' : 'dark',/" src/config.ts; git add src/config.ts
commit "Priya Nair" "fix(config): default to the dark theme"
a test/store.test.ts <<'EOF'

test('returns undefined for a missing note', () => {
  expect(new NoteStore().get('missing')).toBeUndefined();
});
EOF
commit "Priya Nair" "test(core): missing notes"
git push -q origin fix/config-defaults

# ── feature/export: fixup + wip commits, made for interactive rebase ───────
git checkout -q main
git checkout -q -b feature/export
w src/export/html.ts <<'EOF'
import type { Note } from '../note.js';

export function toHtml(note: Note): string {
  return `<article><h1>${note.title}</h1><pre>${note.body}</pre></article>`;
}
EOF
commit "Leo Okafor" "feat(export): export a note as HTML"
sed -i 's|<h1>${note.title}</h1>|<h1>${escape(note.title)}</h1>|; s|<pre>${note.body}</pre>|<pre>${escape(note.body)}</pre>|' src/export/html.ts
a src/export/html.ts <<'EOF'

function escape(text: string): string {
  return text.replace(/[&<>"]/g, (c) => `&#${c.charCodeAt(0)};`);
}
EOF
commit "Leo Okafor" "fixup! feat(export): export a note as HTML"
w src/export/bundle.ts <<'EOF'
import type { Note } from '../note.js';
import { toHtml } from './html.js';

export function bundle(notes: Note[]): string {
  return notes.map(toHtml).join('\n');
}
EOF
commit "Leo Okafor" "wip"
w test/export.test.ts <<'EOF'
import { expect, test } from 'vitest';
import { toHtml } from '../src/export/html.js';

test('escapes HTML', () => {
  const html = toHtml({ id: 'x', title: '<b>', body: '', tags: [], updatedAt: new Date(0) });
  expect(html).toContain('&#60;b&#62;');
});
EOF
commit "Priya Nair" "test(export): escape titles"
a README.md <<'EOF'

## Export

    lumen export --html notes/
EOF
commit "Leo Okafor" "docs(export): document the export command"

# ── main moves on ──────────────────────────────────────────────────────────
git checkout -q main
w src/sync/schedule.ts <<'EOF'
export function nextRun(lastRun: Date, intervalMinutes: number): Date {
  return new Date(lastRun.getTime() + intervalMinutes * 60_000);
}
EOF
commit "Leo Okafor" "feat(sync): schedule the next sync"
a test/markdown.test.ts <<'EOF'

test('counts words', async () => {
  const { wordCount } = await import('../src/markdown.js');
  expect(wordCount('one two  three')).toBe(3);
});
EOF
commit "Priya Nair" "test(markdown): word count"
sed -i 's/console.log(`lumen: notes in ${config.notesDir}`);/console.log(`lumen ${process.argv[2] ?? "help"}: notes in ${config.notesDir}`);/' src/cli.ts; git add src/cli.ts
commit "Maya Chen" "refactor(cli): print the subcommand"
w CHANGELOG.md <<'EOF'
# Changelog

## 1.0.0
- Full-text search
- Dark mode
EOF
commit "Maya Chen" "docs: add a changelog"
a src/tags.ts <<'EOF'

export function uniqueTags(tags: string[]): string[] {
  return [...new Set(tags.map(normalizeTag))];
}
EOF
commit "Omar Haddad" "feat(core): de-duplicate tags"
git push -q origin main

# ── feature/sync-ui: in progress, pushed ───────────────────────────────────
git checkout -q -b feature/sync-ui
w src/sync/status.ts <<'EOF'
export type SyncStatus = 'idle' | 'syncing' | 'error';

export function label(status: SyncStatus): string {
  return { idle: 'Up to date', syncing: 'Syncing…', error: 'Sync failed' }[status];
}
EOF
commit "Sara Lindqvist" "feat(sync): status labels"
a src/sync/status.ts <<'EOF'

export const RETRY_AFTER_MS = 30_000;
EOF
commit "Sara Lindqvist" "feat(sync): retry after a failure"
git push -q -u origin feature/sync-ui

git checkout -q main
a src/store.ts <<'EOF'

export function search(notes: Note[], tag: string): Note[] {
  return notes.filter((n) => n.tags.includes(tag));
}
EOF
commit "Leo Okafor" "feat(core): filter notes by tag"
# Local-only commit: main is one ahead of origin/main.
sed -i 's/Fast, local Markdown notes with full-text search./Fast, local Markdown notes with full-text search, tags and sync./' README.md; git add README.md
commit "Maya Chen" "docs: mention tags and sync"
git branch -q --set-upstream-to=origin/main main

echo "demo repo: $REPO ($(git rev-list --all --count) commits, $(git branch | wc -l) branches, origin at $REMOTE)"
