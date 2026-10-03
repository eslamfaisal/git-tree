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

Tier 2 needs `git lfs` and network access to `lfs.github.com`. The sandboxed session that builds the course cannot
reach it (its network policy denies that host). So the **final 1080p lesson video of each episode is committed as a plain
git file** at `assets/<series>/<id>-<slug>/video/<id>-<slug>.1080p.mp4` (about 10 to 15 MB each, validator limit 50 MB),
next to its subtitles, chapters and `manifest.json`; `.gitattributes` exempts exactly that pattern from LFS. Voice-over
stems (FLAC) stay out of git; their size and sha256 are in the manifest.

To move the videos into LFS later (from a normal machine, once the repo holds about 500 MB of video):

```bash
git lfs install
git lfs migrate import --include="course/assets/**/*.1080p.mp4" --everything
```

and delete the exemption line from `.gitattributes` in the same commit.

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
