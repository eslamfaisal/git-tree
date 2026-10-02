# SEO and channel plan (English)

## Channel

One channel, one language. Playlists: one per series, plus learning paths (Beginner, Moving from the command line,
Team lead) and a "Fix it" playlist of task-titled videos. A channel trailer and a trailer per series.

## Title rules

- 60 characters or fewer; the search phrase first; no clickbait; no other product's name.
- Example: `Stage a single hunk in GitTree (commit part of a file)`.

## Description template (the first 150 characters carry the keyword and the promise)

```
<promise sentence, with the search phrase>

Chapters: <from <episode>.chapters.txt>
Follow along: course/demo-repo/build.sh <checkpoint>  (https://github.com/eslamfaisal/git-tree/tree/main/course)
Download GitTree free: https://gittree.app/en/download?utm_source=youtube&utm_medium=video&utm_campaign=<episode-id>
Equivalent git commands: ...
Next video: <link>
The narrator's voice is a synthetic voice made from the author's own voice.
GitTree is not affiliated with any other Git client.
```

On upload, turn on YouTube's *altered or synthetic content* option (the voice is realistic and synthetic).

## Tags, cards, end screens

8 to 15 tags per video: the feature, the Git concept, the git command, `GitTree`, `git gui`, the platform. One card at
the moment the next lesson is mentioned; the end screen shows the next episode and the playlist.

## Keywords (per episode, in `episode.yml` under `keywords:`)

A primary phrase, two secondary phrases and one long-tail question, for example for 02-02: `git stage hunk` /
`git add -p`, `commit part of a file`, `partial commit`, "how do I commit only part of a file in git". Refined with
search-suggest data before each upload.

## Measurement

Every description link carries `utm_campaign=<episode-id>`; per video: click-through rate, average view duration,
downloads attributed to the UTM, and comments asking for corrections (they go to the issue forms).

## Publishing

Upload is manual or through the YouTube Data API; credentials never enter this repository. After upload, write the video
id into the episode's `episode.yml` (`youtube:`) and regenerate the README table. See `../publishing/` for the other
platforms.
