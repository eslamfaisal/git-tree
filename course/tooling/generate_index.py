#!/usr/bin/env python3
"""Regenerates the episode table in course/README.md and course/episodes.json from the episode.yml files.

    generate_index.py [--check]     --check fails when the committed files are out of date (CI).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

COURSE = Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- episodes:begin -->", "<!-- episodes:end -->"


def load() -> list[dict]:
    out = []
    for f in sorted((COURSE / "curriculum").rglob("episode.yml")):
        m = yaml.safe_load(f.read_text())
        m["path"] = str(f.parent.relative_to(COURSE))
        out.append(m)
    return sorted(out, key=lambda m: m["id"])


def series_summary(eps: list[dict]) -> str:
    plan = yaml.safe_load((COURSE / "curriculum.yml").read_text())
    rows = ["| Series | Episodes | Published |", "|---|---|---|"]
    for s in plan["series"]:
        mine = [m for m in eps if m["series"] == s["id"]]
        pub = sum(1 for m in mine if m.get("status") == "published")
        rows.append(f"| {s['title_en']} | {len(mine)} | {pub} |")
    rows.append(f"| **Total** | **{len(eps)}** | **{sum(1 for m in eps if m.get('status') == 'published')}** |")
    return "\n".join(rows)


def table(eps: list[dict]) -> str:
    rows = ["| Episode | Series | Status | English | العربية |", "|---|---|---|---|---|"]
    for m in eps:
        yt = m.get("youtube") or {}
        link = lambda v: f"[watch](https://youtu.be/{v})" if v else "not yet published"  # noqa: E731
        rows.append(f"| [{m['id']} · {m['title']['en']}]({m['path']}/) | {m['series'].split('-', 1)[1].replace('-', ' ')} | {m['status']} | {link(yt.get('en'))} | {link(yt.get('ar'))} |")
    return "\n".join(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ns = ap.parse_args()
    eps = load()
    def splice(path: Path, body: str) -> str:
        text = path.read_text()
        if BEGIN not in text:
            print(f"{path.name} has no episodes block", file=sys.stderr)
            sys.exit(1)
        return text[: text.index(BEGIN)] + f"{BEGIN}\n{body}\n{END}" + text[text.index(END) + len(END):]

    readme = (COURSE / "README.md").read_text()
    new = splice(COURSE / "README.md", series_summary(eps))
    cur_path = COURSE / "curriculum" / "README.md"
    cur_new = splice(cur_path, table(eps))
    cur_old = cur_path.read_text()
    index = json.dumps([{k: m[k] for k in ("id", "series", "slug", "status", "title", "promise", "feature", "concept", "commands", "checkpoint", "youtube", "path") if k in m} for m in eps], indent=1, ensure_ascii=False) + "\n"
    if ns.check:
        stale = new != readme or cur_new != cur_old or not (COURSE / "episodes.json").exists() or (COURSE / "episodes.json").read_text() != index
        print("course index is " + ("OUT OF DATE: run tooling/generate_index.py" if stale else "current"))
        sys.exit(1 if stale else 0)
    (COURSE / "README.md").write_text(new)
    cur_path.write_text(cur_new)
    (COURSE / "episodes.json").write_text(index)
    print(f"{len(eps)} episode(s) indexed")


if __name__ == "__main__":
    main()
