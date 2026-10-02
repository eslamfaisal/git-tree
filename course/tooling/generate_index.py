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
    readme = (COURSE / "README.md").read_text()
    block = f"{BEGIN}\n{table(eps)}\n{END}"
    if BEGIN in readme:
        new = readme[: readme.index(BEGIN)] + block + readme[readme.index(END) + len(END):]
    else:
        print("README.md has no episodes block", file=sys.stderr)
        sys.exit(1)
    index = json.dumps([{k: m[k] for k in ("id", "series", "slug", "status", "title", "promise", "feature", "concept", "commands", "checkpoint", "youtube", "path") if k in m} for m in eps], indent=1, ensure_ascii=False) + "\n"
    if ns.check:
        stale = new != readme or not (COURSE / "episodes.json").exists() or (COURSE / "episodes.json").read_text() != index
        print("course index is " + ("OUT OF DATE: run tooling/generate_index.py" if stale else "current"))
        sys.exit(1 if stale else 0)
    (COURSE / "README.md").write_text(new)
    (COURSE / "episodes.json").write_text(index)
    print(f"{len(eps)} episode(s) indexed")


if __name__ == "__main__":
    main()
