#!/usr/bin/env python3
"""Creates (or refreshes the planning fields of) every episode folder from course/curriculum.yml.

    scaffold_episodes.py            new episodes get an episode.yml with status "planned"; existing ones keep their status
                                    and content (only the planning fields are not touched at all)
    scaffold_episodes.py --check    fails when curriculum.yml lists an episode that has no folder

Also writes demo-repo/PLANNED.md: the checkpoints the planned episodes need and the episodes that need them.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

COURSE = Path(__file__).resolve().parent.parent


def main() -> None:
    plan = yaml.safe_load((COURSE / "curriculum.yml").read_text())
    check = "--check" in sys.argv
    missing, needs = [], defaultdict(list)
    for e in plan["episodes"]:
        folder = COURSE / "curriculum" / e["series"] / e["slug"]
        existing = {p.stem for p in (COURSE / "demo-repo" / "checkpoints").glob("*.sh")}
        if e["checkpoint"] not in existing:
            needs[e["checkpoint"]].append(e["id"])
        if (folder / "episode.yml").exists():
            continue
        missing.append(e["id"])
        if check:
            continue
        folder.mkdir(parents=True, exist_ok=True)
        meta = {
            "id": e["id"], "series": e["series"], "slug": e["slug"], "status": "planned",
            "title": {"en": e["title_en"], "ar": e["title_ar"]},
            "promise": {"en": e["promise_en"]},
            "concept": e["concept"], "feature": e["feature"], "commands": e["commands"],
            "checkpoint": e["checkpoint"], "journey": e["slug"], "duration_min": e["duration_min"],
            "requires": e["requires"], "platforms": e["platforms"],
        }
        if e.get("notes"):
            meta["notes"] = e["notes"]
        meta["youtube"] = {"en": None, "ar": None}
        (folder / "episode.yml").write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=120))
    lines = ["# Planned checkpoints", "", "Checkpoints that planned episodes name but `checkpoints/` does not yet contain. Each becomes",
             "`checkpoints/<name>.sh` when the first episode that needs it is scripted.", "",
             "| Checkpoint | Episodes |", "|---|---|"]
    lines += [f"| `{name}` | {', '.join(ids)} |" for name, ids in sorted(needs.items(), key=lambda kv: -len(kv[1]))]
    if not check:
        (COURSE / "demo-repo" / "PLANNED.md").write_text("\n".join(lines) + "\n")
    print(f"{len(plan['episodes'])} episodes in the plan, {len(missing)} without a folder{' (created)' if not check else ''}, {len(needs)} checkpoints still to build")
    sys.exit(1 if (check and missing) else 0)


if __name__ == "__main__":
    main()
