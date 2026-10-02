# Authoring an episode

An episode is a folder `curriculum/<series>/<slug>/` with `episode.yml` (plan and publishing data), `beats.yml` (the
script and what is on screen), `journey.mjs` (the recorded GitTree session) and, rarely, `scenes/*.html`. Look at the
pilot, `curriculum/02-daily-workflow/stage-a-single-hunk/`, for every file below.

## Rules

- One video, one feature. 2 to 4 minutes (about 250 to 420 spoken words). The first 8 seconds state the problem.
- Everything shown is true and verified: labels come from `apps/desktop/src/app/i18n/en.ts` in `open-git-tree`, shortcuts
  from `tooling/contract-snapshots/ui-commands-contract.json`, every git command and its output from running it in the
  checkpoint repo. Anything unconfirmed goes in `episode.yml` `notes:` and the verify list, never into the script.
- No other product's name. English only. The narrator speaks plain sentences: short, active, no jargon unexplained.
- Layout: no text over text or over the app UI. `tooling/scene_lint.py` checks scenes; the app is framed so the step label
  and the author bubble never cover it. Camera views cut at panel borders, never through a word.

## episode.yml (fields beyond the plan)

`status: scripted`, `recorded_against`, `objectives` (3+), `keywords {primary, secondary[], question}`, `takeaways`,
`quiz` (3+ questions: `q`, `options` (3+), `answer` index, `why`), `exercise {checkpoint, steps[], expected}`,
`commands_note`, `social.hook`. `tooling/validate_course.py` enforces them.

## beats.yml

```yaml
beats:
  - id: hook                       # unique; becomes the audio file name for a real recording (audio/<id>.wav)
    chapter: "Why ..."             # optional: YouTube chapter title (the first becomes 0:00)
    scene: {template: hook, data: {...}}     # a template (below), or  scene: name  for scenes/name.html
    vo: "Spoken words. {git add -p|git add dash p} shows the caption text and speaks the respelling."
  - id: do-it
    app:                           # a span of the recorded journey, between two markers
      from: marker-a
      to: marker-b
      camera: full                 # or {center: [776, 330], zoom: 1.27}  (window px, 1280x720)
    overlays:                      # drawn over the app footage
      - {type: step, n: 1, text: "Open the working changes"}              # the numbered label under the window
      - {type: box, rect: marker-rect, from: m1, to: m2, pad: 4, color: [176, 124, 240]}   # outline around a marked element
      - {type: keys, keys: ["Ctrl", "Shift", "P"], from: m1, to: m2}      # key caps
    vo: "..."
```

Contiguous `app` beats are one continuous screen recording; the footage speed is set so it lasts as long as the words
(slow or hold when the words are longer). Keep the words and the footage aligned by putting markers where each beat starts.
`vo` sentences are synthesised one by one; a fragment under three words is joined to its neighbour.

### Scene templates (`visuals/templates/*.html`, sample data in `templates/samples/*.json`)

| template | data |
|---|---|
| `hook` | `tag`, `kicker`, `title`, `subtitle`, `question`, optional `snippet {file, lines[[kind(ctx/add/del), number, text]]}` |
| `cards` | `tag`, `title`, `cards[{label, title, text, highlight}]` (2 to 4), `footer` |
| `steps` | `tag`, `title`, `steps[]` (HTML allowed: `<b>`, `<code>`) |
| `terminal` | `tag`, `cwd`, `lines[{k: cmd/dim/add/del/hunk/q, t}]`, `keys[[key, meaning]]`, `note` |
| `compare` | `tag`, `title`, `gittree[]`, `terminal[]` |
| `graph` | `tag`, `title`, `nodes[{id, x(0-8), lane(0-3), at, label}]`, `edges[[from, to, at]]`, `refs[{name, node, at, color}]`, `caption` (`at` = start as a fraction 0-1 of the scene) |
| `recap` | `tag`, `points[]` (2 to 4), `next` |

A typical lesson: `hook` (problem) -> optional `cards`/`graph` (idea) -> app beats (do it) -> `terminal` (the same in
plain git, with the real output) -> `recap` (with the next lesson). Write a custom `scenes/<name>.html` only when no
template fits (copy a template as the starting point and keep the `data-i` / `window.TEXT` pattern).

Chapters: give one `chapter` per idea (6 to 10 per video).

## journey.mjs

A default export `{name, wip: false, quietTooltips: true, park: {x, y}, prepare(ui), run(ui)}`. `ui` is
`scripts/demo/lib/ui.mjs` of open-git-tree: `find(role, name)`, `click(role, name, {after})`, `clickSelector`,
`hoverSelector`, `shiftClickSelector`, `type`, `keys`, `dialog`, `mark(name, selectorOrRect)`, `sleep`, `queryAll`.
Mark the start of every beat (`await ui.mark('open-changes')`) and every element a box will outline (`ui.mark('hunk1', selector)`).
Give each beat enough dwell time (`ui.sleep`) for its words: about 2.2 seconds per 8 words.

Test it without capture (about 40 seconds):

```bash
cd open-git-tree/scripts/demo
OGT_DEMO_WIDTH=1280 OGT_DEMO_HEIGHT=720 OGT_DEMO_SCALE=3 OGT_DEMO_PORT=4800 \
  dbus-run-session -- xvfb-run -a -s "-screen 0 3840x2160x24 -nolisten tcp" \
  node record.mjs <journey-name> --journey <path>/journey.mjs --repo-script <path>/course/demo-repo/build.sh \
  --repo-arg <checkpoint> --no-capture --work /tmp/jtest-<name>
```

Record and build are done by `tooling/compose.py` (`--record`, then without it).

## Checkpoints

`demo-repo/checkpoints/<name>.sh` runs inside the freshly built `lumen` repo (`$REPO`) and creates the starting state of an
episode (see `two-hunks.sh`). List: `demo-repo/build.sh --list`; needed ones: `demo-repo/PLANNED.md`. Build, run the
episode's git commands, and capture their real output for the `terminal` scene.

## Check

```bash
python3 course/tooling/validate_course.py && python3 course/tooling/generate_index.py && python3 course/tooling/publish.py
```
