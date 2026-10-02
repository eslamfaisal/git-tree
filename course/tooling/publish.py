#!/usr/bin/env python3
"""Builds the publishing pack from course/publishing/course.yml, curriculum.yml and the episode files.

    publish.py [--check]

Writes course/publishing/out/:
  youtube/<id>-<slug>.md            title, description with chapters, tags, pinned comment (scripted episodes)
  youtube/playlists.md              one playlist per section, in lecture order
  udemy/course-landing.md           title, subtitle, description, what you will learn, requirements, audience
  udemy/curriculum.md and .csv      sections and lectures with descriptions, objectives and lengths
  udemy/quizzes.md                  every lecture's quiz, grouped by section
  linkedin-learning/proposal.md     course proposal: audience, objectives, chapter and video outline
  social/<id>-<slug>.md             LinkedIn post, X post and a Short script per episode that has social text
  transcripts/<id>-<slug>.txt       the spoken words by chapter (scripted episodes)
  resources/cheatsheet-<section>.md the git commands taught in a section
  README.md                         what is complete and what is still planned

With --check, fails when the committed files differ from what would be generated (CI).
"""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
sys.path.insert(0, str(HERE))
import scripttext as voice  # noqa: E402  (display_text, sentences)

OUT = COURSE / "publishing" / "out"
REPO = "https://github.com/eslamfaisal/git-tree/tree/main/course"


def load():
    course = yaml.safe_load((COURSE / "publishing" / "course.yml").read_text())
    plan = yaml.safe_load((COURSE / "curriculum.yml").read_text())
    eps = []
    for e in plan["episodes"]:
        folder = COURSE / "curriculum" / e["series"] / e["slug"]
        meta = yaml.safe_load((folder / "episode.yml").read_text())
        meta["folder"] = folder
        eps.append(meta)
    eps.sort(key=lambda m: m["id"])
    return course, plan, eps


def stem(m) -> str:
    return f"{m['id']}-{m['slug']}"


def chapters_of(m) -> str:
    """YouTube chapters: from the built video's chapters file when present, else from the beats' chapter titles."""
    for p in (COURSE / "assets" / m["series"] / stem(m) / "video" / f"{stem(m)}.chapters.txt", COURSE / ".work" / m["id"] / "out" / f"{stem(m)}.chapters.txt"):
        if p.exists():
            return p.read_text().rstrip()
    return ""


def is_scripted(m) -> bool:
    return m["status"] != "planned" and (m["folder"] / "beats.yml").exists()


def next_of(m, eps):
    mine = [e for e in eps if e["series"] == m["series"]]
    i = mine.index(m)
    return mine[i + 1] if i + 1 < len(mine) else None


def tags_of(m) -> list[str]:
    k = m.get("keywords") or {}
    base = [k.get("primary"), *(k.get("secondary") or []), "GitTree", "git gui", "git tutorial", "git for beginners", "visual git client"]
    base += [c.replace("git ", "git ", 1) for c in m.get("commands", [])[:2]]
    seen, out = set(), []
    for t in base:
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out[:15]


def youtube(m, eps) -> str:
    nxt = next_of(m, eps)
    ch = chapters_of(m)
    cmds = "\n".join(m.get("commands", []))
    desc = f"""{m['promise']} {m.get('concept', '')}

{('Chapters' + chr(10) + ch + chr(10)) if ch else ''}
Follow along with the same repository:
course/demo-repo/build.sh ~/lumen {m['checkpoint']}
{REPO}

Download GitTree free for macOS, Windows and Linux:
https://gittree.app/en/download?utm_source=youtube&utm_medium=video&utm_campaign={m['id']}

Equivalent git commands
{cmds}

{('Next lesson: ' + nxt['title']) if nxt else ''}
The narration is a synthetic voice (text to speech).
GitTree is not affiliated with any other Git client."""
    k = m.get("keywords") or {}
    return f"""# {stem(m)}

**Title** ({len(m['title'])} characters): `{m['title']}`

**Description**

```
{desc.strip()}
```

**Tags**: {', '.join(tags_of(m))}

**Hashtags**: #GitTree #Git #GitTutorial

**Pinned comment**: `Try it yourself: course/demo-repo/build.sh ~/lumen {m['checkpoint']}, then open the folder in GitTree. What will you commit first?`

**Primary keyword**: {k.get('primary', '')} · **Question**: {k.get('question', '')}

**Upload settings**: altered or synthetic content = yes (synthetic voice); playlist = section "{m['series']}"; thumbnail = `curriculum/{m['series']}/{m['slug']}/thumbnail/thumbnail.jpg`; captions = the episode's `.srt`.
"""


def lecture_description(m) -> str:
    obj = "\n".join(f"- {o}" for o in m.get("objectives", []))
    return f"{m['promise']}\n\nBy the end of this lecture you can:\n{obj}" if obj else m["promise"]


def build() -> dict[str, str]:
    course, plan, eps = load()
    files: dict[str, str] = {}
    sections = {s["id"]: s for s in plan["series"]}
    extra = {s["id"]: s for s in course["sections"]}
    minutes = sum(m["duration_min"] for m in eps)
    n = len(eps)

    # YouTube
    pl = ["# YouTube playlists", "", "One playlist per section, in lecture order, plus the full course in the same order.", ""]
    for sid, s in sections.items():
        mine = [m for m in eps if m["series"] == sid]
        pl += [f"## {s['title_en']}", "", s["summary_en"], ""] + [f"{i}. {m['title']} ({m['id']}, {m['status']})" for i, m in enumerate(mine, 1)] + [""]
    files["youtube/playlists.md"] = "\n".join(pl)
    for m in eps:
        if is_scripted(m):
            files[f"youtube/{stem(m)}.md"] = youtube(m, eps)

    # Udemy
    lines = [f"# {course['title']}", "", f"**Subtitle**: {course['subtitle']}", "", "## Description", "", course["description"].strip(), "", "## What you'll learn", ""]
    lines += [f"- {o}" for o in course["outcomes"]] + ["", "## Requirements", ""] + [f"- {r}" for r in course["requirements"]]
    lines += ["", "## Who this course is for", ""] + [f"- {a}" for a in course["audience"]]
    lines += ["", f"**Level**: {course['level']} · **Language**: {course['language']} · **Lectures**: {n} · **Video**: about {minutes / 60:.1f} hours", "", f"**Instructor**: {course['instructor']['name']}, {course['instructor']['title']}. {course['instructor']['bio']}", ""]
    files["udemy/course-landing.md"] = "\n".join(lines)
    cur, rows, quiz = ["# Curriculum", ""], [["section", "lecture", "id", "title", "minutes", "status", "description"]], ["# Quizzes", ""]
    for si, (sid, s) in enumerate(sections.items(), 1):
        mine = [m for m in eps if m["series"] == sid]
        cur += [f"## Section {si}: {s['title_en']}", "", f"*{extra[sid]['outcome']}*", ""]
        quiz += [f"## Section {si}: {s['title_en']}", ""]
        for li, m in enumerate(mine, 1):
            cur += [f"### {si}.{li} {m['title']}", f"{m['duration_min']} min · {m['id']} · {m['status']}", "", lecture_description(m), ""]
            rows.append([si, li, m["id"], m["title"], m["duration_min"], m["status"], lecture_description(m).replace("\n", " ")])
            for qi, q in enumerate(m.get("quiz", []), 1):
                quiz += [f"**{m['id']} Q{qi}. {q['q']}**", ""] + [f"{chr(97 + i)}) {o}{'  ✓' if i == q['answer'] else ''}" for i, o in enumerate(q["options"])] + ["", f"*{q['why']}*", ""]
    files["udemy/curriculum.md"] = "\n".join(cur)
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    files["udemy/curriculum.csv"] = buf.getvalue()
    files["udemy/quizzes.md"] = "\n".join(quiz)

    # LinkedIn Learning
    p = [f"# Course proposal: {course['title']}", "", f"**Subtitle**: {course['subtitle']}", "", "## Audience", ""] + [f"- {a}" for a in course["audience"]]
    p += ["", "## Prerequisites", ""] + [f"- {r}" for r in course["requirements"]] + ["", "## Learning objectives", ""] + [f"- {o}" for o in course["outcomes"]]
    p += ["", "## Exercise files", "", f"- The practice repository: `{REPO}/demo-repo` (one start state per lecture)", "", "## Outline", ""]
    for si, (sid, s) in enumerate(sections.items(), 1):
        mine = [m for m in eps if m["series"] == sid]
        p += [f"### Chapter {si}: {s['title_en']} ({sum(m['duration_min'] for m in mine):g} min)", "", extra[sid]["outcome"], ""] + [f"- {m['title']} ({m['duration_min']:g} min)" for m in mine] + [""]
    files["linkedin-learning/proposal.md"] = "\n".join(p)

    # social, transcripts, cheat sheets
    for m in eps:
        s = m.get("social")
        if s:
            files[f"social/{stem(m)}.md"] = f"""# {stem(m)}: social posts

**LinkedIn**

{s['hook']}

Lesson: {m['title']} ({m['duration_min']:g} min). Free, with a practice repository to follow along.

#Git #GitTree #SoftwareEngineering #DeveloperTools

**X / short post**

{s['hook']} {m['title']}. #Git #GitTree

**YouTube Short (30 to 45 seconds)**

1. Hook (0-5 s): "{s['hook']}"
2. Show the key step in GitTree on screen: {(m.get('objectives') or [m['promise']])[1 if len(m.get('objectives', [])) > 1 else 0]}
3. Result (last 8 s): "{m['promise']} Full lesson on the channel."
"""
        if is_scripted(m):
            beats = yaml.safe_load((m["folder"] / "beats.yml").read_text())["beats"]
            t = [f"{m['title']}", ""]
            for b in beats:
                if b.get("chapter"):
                    t += ["", f"[{b['chapter']}]"]
                t.append(" ".join(voice.display_text(s) for s in voice.sentences(b["vo"])))
            files[f"transcripts/{stem(m)}.txt"] = "\n".join(t) + "\n"
    for sid, s in sections.items():
        cmds: dict[str, str] = {}
        for m in eps:
            if m["series"] == sid:
                for c in m.get("commands", []):
                    cmds.setdefault(c, m["title"])
        if cmds:
            files[f"resources/cheatsheet-{sid}.md"] = f"# Commands: {s['title_en']}\n\n| Command | Lesson |\n|---|---|\n" + "\n".join(f"| `{c}` | {t} |" for c, t in cmds.items()) + "\n"

    full = [m for m in eps if is_scripted(m) and m.get("objectives") and m.get("quiz")]
    files["README.md"] = f"""# Publishing pack (generated)

Run `python3 course/tooling/publish.py` after changing `course.yml`, `curriculum.yml` or an episode file.

| | |
|---|---|
| Lectures planned | {n} |
| Lectures with a script | {sum(1 for m in eps if is_scripted(m))} |
| Lectures with objectives, quiz and exercise (ready to publish) | {len(full)} |
| Video, planned length | about {minutes / 60:.1f} hours |

- `youtube/`: per-video metadata and the playlists
- `udemy/`: landing page, curriculum (md and csv), quizzes
- `linkedin-learning/`: the course proposal outline
- `social/`: posts and Short scripts per lecture
- `transcripts/`, `resources/`: transcripts and per-section command cheat sheets

Platform requirements change; check each platform's current rules before submitting (see `../course.yml`, `platform_notes`).
"""
    return files


def main() -> None:
    files = build()
    if "--check" in sys.argv:
        stale = [p for p, t in files.items() if not (OUT / p).exists() or (OUT / p).read_text() != t]
        extra = [str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file() and str(p.relative_to(OUT)) not in files] if OUT.exists() else []
        print("publishing pack " + (f"OUT OF DATE: {len(stale)} stale, {len(extra)} extra; run tooling/publish.py" if stale or extra else "is current"))
        sys.exit(1 if stale or extra else 0)
    if OUT.exists():
        for p in sorted(OUT.rglob("*"), reverse=True):
            p.unlink() if p.is_file() else p.rmdir()
    for rel, text in files.items():
        path = OUT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text if text.endswith("\n") else text + "\n")
    print(f"{len(files)} files in {OUT.relative_to(COURSE.parent)}")


if __name__ == "__main__":
    main()
