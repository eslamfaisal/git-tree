# Learn GitTree: the video course

A free video course that teaches Git from first principles **and** shows how to do every task in
[GitTree](https://gittree.app), the visual Git client for macOS, Windows and Linux. It is in **English**.

**One video, one lesson.** Every video teaches exactly one Git idea and the one GitTree feature that does it, in
3 to 10 minutes. Each stands alone, so you can watch just the one you need. Playlists give the order.

> Status: **170 videos planned, 1 in production** (the pilot, 02-02, is being reviewed before the rest are produced).
> The plan is [`curriculum.yml`](curriculum.yml), the per-episode list is in [`curriculum/`](curriculum/README.md), the
> structure is explained in [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Start here

<!-- episodes:begin -->
| Series | Episodes | Published |
|---|---|---|
| Start here: install, sign in, open a repository | 13 | 0 |
| Git foundations: the ideas behind every click | 12 | 0 |
| Daily workflow: stage, commit, review | 30 | 0 |
| Branching and merging | 20 | 0 |
| Rewriting history and getting out of trouble | 19 | 0 |
| Collaboration: remotes, pull requests, providers | 29 | 0 |
| Power features: worktrees, submodules, LFS, search | 26 | 0 |
| Customise GitTree and fix problems | 20 | 0 |
| **Total** | **169** | **0** |
<!-- episodes:end -->

## What is in this folder

| Path | What |
|---|---|
| [`curriculum/`](curriculum/) | One folder per episode: script, shot list, visuals, commands, metadata |
| [`demo-repo/`](demo-repo/) | The teaching repository every episode starts from, one named checkpoint each |
| [`assets/`](assets/) | Videos, voice-over, thumbnails, project files, downloads (Git LFS) |
| [`visuals/`](visuals/) | The scene kit: diagrams and motion graphics as HTML and CSS |
| [`audio/`](audio/) | Voice brief for the speakers, pronunciation list, loudness spec |
| [`seo/`](seo/) | Channel, playlists, keywords, title and description rules |
| [`qa/`](qa/) | The review checklist and the review log |
| [`tooling/`](tooling/) | Build, lint and quality scripts |
| [`inventory.md`](inventory.md) | Every GitTree feature, checked against the app |
| [`glossary.md`](glossary.md) | Pronunciation list for the technical terms in the scripts |

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
