# Course architecture

This folder is the single home of the GitTree video course: the plan, every script and diagram, the recordings, the
voice-over and the published videos. YouTube is where people watch; this repository is the archive and the source.

## Principles

1. **One video, one lesson.** One Git concept and exactly one GitTree feature per video (`feature:` in `episode.yml` is a
   single id; `tooling/validate_course.py` rejects a list). A feature with sub-tasks becomes several short videos
   (stage a file, stage a hunk, stage lines). Playlists, not long videos, provide the sequence. A prerequisite is a link
   and one sentence, never a re-teach.
2. **Real app only.** Every GitTree shot is recorded from the actual app by the pipeline in
   `open-git-tree/scripts/demo`; there are no mock-ups. Every git command shown was run in the demo repository.
3. **Accuracy first.** `inventory.md` lists each feature with its source in the app and its status. Anything not shipped
   is excluded; anything unconfirmed is on `verify-list.md`.
4. **English only.** One script, one voice, one set of captions per episode. The narrator is the author's own voice,
   cloned from a recording sample (`tooling/voice_clone.py`); a real recording of any beat replaces it.
5. **Quality floor: Full HD.** Videos are delivered at 1080p or better (recordings are captured at 2160p), BT.709, 30 fps,
   -14 LUFS. `tooling/quality.py` checks every delivered file.
6. **Nothing only on a laptop.** Every asset lives in this repository (`assets/`), in the storage tier its size needs.

## Layout

```
course/
  README.md  ARCHITECTURE.md  CONTRIBUTING.md  inventory.md  glossary.md  verify-list.md  roadmap.md  CHANGELOG.md
  curriculum/<NN>-<series>/<slug>/       one folder per episode (episode id = <series number>-<order>)
    episode.yml                          id, status, title, concept, feature, commands, checkpoint, journey, YouTube ids
    beats.yml                            the script: per beat the words and the picture (scene or app span)
    journey.mjs                          the recorded real-app journey (markers the beats refer to)
    scenes/*.html                        diagram scenes for this episode
    metadata.md                          title, description, chapters, tags, pinned comment, thumbnail brief
  assets/<series>/<id>-<slug>/           video/, audio/, thumbnails/, projects/, manifest.json
  assets/shared/  assets/downloads/      intro/outro, music (with licences), fonts · demo-repo bundle, cheat sheets
  demo-repo/                             build.sh, lumen-history.sh, checkpoints/<name>.sh
  visuals/kit/                           scene.css, kit.js, brand assets (the scene runtime)
  audio/  seo/  qa/  presenter/  tooling/
```

## An episode's life

`planned` → `scripted` (beats.yml reviewed) → `recorded` (journey recorded against a pinned GitTree release) →
`reviewed` (QA checklist signed) → `published` (YouTube ids written back).

## How a video is built

```
beats.yml ──► voice (scratch TTS, or the speakers' takes)  ──► per-beat timing
journey.mjs ─► 4K recording of the real app ─► montage: framed window, zoom, cursor, step labels, lecturer
scenes/*.html ─► deterministic frame-by-frame render (1080p+)
                         └──► assembled, encoded H.264, quality gate ──► .mp4 + .srt/.vtt + voice .flac
```

```bash
python3 course/tooling/compose.py course/curriculum/02-daily-workflow/stage-a-single-hunk --record       # once per release
python3 course/tooling/compose.py course/curriculum/02-daily-workflow/stage-a-single-hunk 
```

The recorder and montage engine live in `open-git-tree/scripts/demo` (set `OGT_REPO` to its checkout). See
`tooling/README.md` for requirements.

## Storage

See [`assets/README.md`](assets/README.md): plain git for small text files, Git LFS for media, GitHub Releases for
very large masters, a size budget per episode and a quota guard.
