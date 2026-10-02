# Learn GitTree: the video course

A free video course that teaches Git from first principles **and** shows how to do every task in
[GitTree](https://gittree.app), the visual Git client for macOS, Windows and Linux. It is published in
**English and Arabic**, with a native-speaker voice-over for each.

**One video, one lesson.** Every video teaches exactly one Git idea and the one GitTree feature that does it, in
3 to 10 minutes. Each stands alone, so you can watch just the one you need. Playlists give the order.

> Status: pilot. The first episode is being reviewed before the rest are produced. The table below is generated from
> [`curriculum/`](curriculum/); the full plan is in [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Start here

<!-- episodes:begin -->
| Episode | Series | Status | English | العربية |
|---|---|---|---|---|
| [02-02 · Stage a single hunk in GitTree (commit part of a file)](curriculum/02-daily-workflow/stage-a-single-hunk/) | daily workflow | scripted | not yet published | not yet published |
<!-- episodes:end -->

## What is in this folder

| Path | What |
|---|---|
| [`curriculum/`](curriculum/) | One folder per episode: script, shot list, visuals, commands, metadata, in both languages |
| [`demo-repo/`](demo-repo/) | The teaching repository every episode starts from, one named checkpoint each |
| [`assets/`](assets/) | Videos, voice-over, thumbnails, project files, downloads (Git LFS) |
| [`visuals/`](visuals/) | The scene kit: diagrams and motion graphics as HTML and CSS |
| [`audio/`](audio/) | Voice brief for the speakers, pronunciation list, loudness spec |
| [`seo/`](seo/) | Channel, playlists, keywords, title and description rules |
| [`qa/`](qa/) | The review checklist and the review log |
| [`tooling/`](tooling/) | Build, lint and quality scripts |
| [`inventory.md`](inventory.md) | Every GitTree feature, checked against the app |
| [`glossary.md`](glossary.md) | English and Arabic terms used in the scripts |

## Follow along

Every episode names the checkpoint it starts from. Build it and open the folder in GitTree:

```bash
course/demo-repo/build.sh ~/lumen two-hunks      # the checkpoint of episode 02-02
course/demo-repo/build.sh --list                 # all checkpoints
```

## Download GitTree

[macOS](https://gittree.app/api/download/macos) · [Windows](https://gittree.app/api/download/windows) ·
[Linux](https://gittree.app/api/download/linux) · [Website](https://gittree.app)

GitTree is not affiliated with, or endorsed by, any other Git client.
