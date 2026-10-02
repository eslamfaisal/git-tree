# Course assets

Every binary and generated asset of the course lives here, so nothing exists only on a laptop. YouTube is the
distribution channel, not the archive.

## Storage tiers

| Tier | What | Limit | How |
|---|---|---|---|
| 1. Plain git | Text and small files: scripts, SRT/VTT, YAML, SVG, thumbnails, PDFs, `manifest.json` | under 1 MB each | normal commit |
| 2. Git LFS | Final and review videos (MP4, WebM), voice-over (WAV, FLAC), mix stems, motion-graphic and editor project files, PSD | under 2 GB each | `.gitattributes` tracks `course/assets/**/*.{mp4,webm,mov,mkv,wav,flac,m4a,mp3,psd,zip}` |
| 3. GitHub Release | Masters above 1 GB, raw lossless screen recordings | none | a release tagged `course-assets-<series>-<n>` (never an app release tag); the episode's `manifest.json` lists name, size, sha256, URL and the command that regenerates it |

GitHub rejects any normal file over 100 MB. The free LFS quota is **1 GB of storage and 1 GB of bandwidth per month**,
so a size budget is kept below and `tooling/validate_course.py` fails on any non-LFS file over 1 MB.

## Publishing media (important)

Tier 2 needs `git lfs` and network access to `lfs.github.com`. The sandboxed session that scaffolded the course
could not reach it (its network policy denies that host), so **no media has been pushed yet**: the pilot's videos were
delivered for review and their size and sha256 are recorded in the episode's `manifest.json`. From a normal machine:

```bash
git lfs install
git add course/assets && git commit -m "feat(course): add 02-02 videos" && git push
```

## Layout

```
assets/<series>/<id>-<slug>/
  video/             <id>-<slug>.1080p.mp4 (+ .captioned.mp4, .srt, .vtt, .chapters.txt)
  audio/             <beat-id>.wav   real recordings, one per beat (they replace the generated voice)
  thumbnails/       final JPEG and its source
  projects/           editor and motion-graphic project files
  manifest.json       every file: size, sha256, tier, how it is regenerated, quality-gate result
assets/shared/        intro and outro, music (with its licence file), fonts
assets/downloads/     the demo-repo bundle, cheat sheets, keymap cards
```

A voice-over take dropped at `audio/<lang>/<beat-id>.wav` is used automatically by `tooling/compose.py` instead of the
scratch voice for that beat.

## Size budget

| Episode | 1080p video | Voice | Total (LFS) |
|---|---|---|---|---|
| 02-02 stage a single hunk | ~20 MB | ~25 MB | ~15 MB | ~60 MB |

Rule of thumb: about 35 MB per episode at 1080p with voice, so the free 1 GB covers roughly 15
episodes. 2160p masters (about 4 times larger) go to Releases, not LFS. **The owner is told before the repository
would exceed the free quota**, to decide on a data pack.
