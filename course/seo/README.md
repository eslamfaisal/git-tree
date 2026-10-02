# SEO and channel plan

## One channel or two

**Recommendation: one channel with two playlists per series (English, Arabic), and the Arabic title written first
in Arabic script.** One channel pools watch time and subscribers, and the video descriptions cross-link both versions.
YouTube's multi-language *audio track* feature is not used: it hides the language from search, and Arabic searchers
look for Arabic titles. Separate channels remain an option if the owner wants separate branding per language.

## Title rules

- 60 characters or fewer; the search phrase first; no clickbait; no other product's name.
- English: `Stage a single hunk in GitTree (commit part of a file)`
- Arabic: written as people search: `كيف تُجهِّز Hunk واحدًا في GitTree وتحفظ جزءًا من الملف`

## Description template (first 150 characters carry the keyword and the promise)

```
<promise sentence, with the search phrase>

Chapters: 0:00 ...
Follow along: course/demo-repo/build.sh <checkpoint>  (https://github.com/eslamfaisal/git-tree/tree/main/course)
Download GitTree free: https://gittree.app/<lang>/download?utm_source=youtube&utm_medium=video&utm_campaign=<episode-id>
Equivalent git commands: ...
Next video: <link>
GitTree is not affiliated with any other Git client.
```

## Tags, cards, end screens

8 to 15 tags per video and language: the feature, the Git concept, the git command, `GitTree`, `git gui`, the platform.
One card at the moment the next lesson is mentioned; the end screen shows the next episode and the playlist.

## Keywords (starting list, to be refined with search-suggest data)

| English | Arabic |
|---|---|
| git stage hunk, git add -p, commit part of a file, partial commit, git gui | شرح git add -p, تقسيم الـ commit, git staging بالعربي, تجهيز جزء من الملف, واجهة git رسومية |

## Measurement

Every description link carries `utm_campaign=<episode-id>`; per video: click-through rate, average view duration,
downloads attributed to the UTM, and comments asking for corrections (they go to the issue forms).

## Publishing

Upload is manual or through the YouTube Data API; credentials never enter this repository. After upload, write the video
ids into the episode's `episode.yml` (`youtube:`) and regenerate the README table.
