#!/usr/bin/env python3
"""Validates the course tree. Exit code 1 on any problem; CI runs it on every pull request.

Checks: episode.yml schema (exactly one `feature`, ids match folders, status in the lifecycle), beats.yml (voice-over
and a scene or app span per beat), English only (no Arabic script anywhere), banned trademark terms, file-size and
storage-tier rules, manifest checksums.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

COURSE = Path(__file__).resolve().parent.parent
STATUSES = ["planned", "scripted", "recorded", "reviewed", "published"]
ARABIC = re.compile("[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff\ufb50-\ufdff\ufe70-\ufeff]")
# Other products' names must not appear in course files (titles, tags, thumbnails, scripts). Built from parts so this
# file does not contain them itself. ('fork' is a Git term and is not on the list.)
BANNED = [re.compile(p, re.I) for p in ("git" + "kraken", "source" + "tree", "git" + "hub desktop", "tower\\b", "smart" + "git")]
LFS_EXT = {".mp4", ".webm", ".mov", ".mkv", ".wav", ".flac", ".m4a", ".mp3", ".psd", ".zip"}
SMALL = 1_000_000
problems: list[str] = []


def bad(msg: str) -> None:
    problems.append(msg)


def episodes() -> list[Path]:
    return sorted(p.parent for p in (COURSE / "curriculum").rglob("episode.yml"))


def check_episode(ep: Path) -> None:
    rel = ep.relative_to(COURSE)
    meta = yaml.safe_load((ep / "episode.yml").read_text())
    for key in ("id", "series", "slug", "status", "title", "promise", "concept", "feature", "commands", "checkpoint", "journey"):
        if key not in meta:
            bad(f"{rel}: episode.yml lacks '{key}'")
    if isinstance(meta.get("feature"), (list, dict)):
        bad(f"{rel}: 'feature' must be exactly one id (one video = one feature), got {meta['feature']!r}")
    if meta.get("status") not in STATUSES:
        bad(f"{rel}: status {meta.get('status')!r} not in {STATUSES}")
    for key in ("title", "promise"):
        if not isinstance(meta.get(key), str) or not meta.get(key):
            bad(f"{rel}: {key} must be a non-empty string")
    if isinstance(meta.get("title"), str) and len(meta["title"]) > 70:
        bad(f"{rel}: title is too long for search results ({len(meta['title'])} characters)")
    if ep.name != meta.get("slug") or not ep.parent.name.startswith(str(meta.get("id", "x")).split("-")[0]):
        bad(f"{rel}: folder does not match slug/series of episode.yml")
    if meta.get("status") != "planned" and not (COURSE / "demo-repo" / "checkpoints" / f"{meta.get('checkpoint')}.sh").exists():
        bad(f"{rel}: checkpoint {meta.get('checkpoint')!r} has no demo-repo/checkpoints script")
    beats_file = ep / "beats.yml"
    if meta.get("status") != "planned":
        if not beats_file.exists():
            bad(f"{rel}: beats.yml missing")
            return
        for beat in yaml.safe_load(beats_file.read_text())["beats"]:
            if not isinstance(beat.get("vo"), str) or not beat["vo"].strip():
                bad(f"{rel}: beat {beat['id']} needs a voice-over string")
            if "scene" in beat and not (ep / "scenes" / f"{beat['scene']}.html").exists():
                bad(f"{rel}: beat {beat['id']} scene '{beat['scene']}' not found")
            if "scene" not in beat and "app" not in beat:
                bad(f"{rel}: beat {beat['id']} has neither scene nor app")


def check_text_files() -> None:
    for path in COURSE.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yml", ".yaml", ".html", ".mjs", ".json", ".css", ".js"} and ".work" not in path.parts and path.name != "validate_course.py":
            text = path.read_text(errors="ignore")
            if ARABIC.search(text):
                bad(f"{path.relative_to(COURSE)}: Arabic script found; the course is English only")
            for pat in BANNED:
                m = pat.search(text)
                if m:
                    bad(f"{path.relative_to(COURSE)}: other product's name or trademark ({m.group(0)!r})")


def lfs_tracked() -> set[str]:
    try:
        out = subprocess.check_output(["git", "lfs", "ls-files", "-n"], cwd=COURSE, text=True, stderr=subprocess.DEVNULL)
        return {line.strip() for line in out.splitlines()}
    except Exception:  # noqa: BLE001
        return set()


def check_sizes() -> None:
    repo = COURSE.parent
    lfs = lfs_tracked()
    for path in (COURSE / "assets").rglob("*"):
        if not path.is_file():
            continue
        rel = str(path.relative_to(repo))
        size = path.stat().st_size
        if path.suffix in LFS_EXT and rel not in lfs and size > 0:
            first = path.read_bytes()[:40]
            if not first.startswith(b"version https://git-lfs"):
                bad(f"{rel}: media must be stored in Git LFS (run 'git lfs track' / commit with LFS installed)")
        elif size > SMALL and rel not in lfs and path.suffix not in LFS_EXT:
            bad(f"{rel}: {size / 1e6:.1f} MB over the 1 MB plain-git limit; use LFS or a Release (assets/README.md)")
    for manifest in (COURSE / "assets").rglob("manifest.json"):
        data = json.loads(manifest.read_text())
        for f in data.get("files", []):
            target = manifest.parent / f["path"]
            if target.exists() and f.get("sha256") and hashlib.sha256(target.read_bytes()).hexdigest() != f["sha256"]:
                bad(f"{target.relative_to(repo)}: sha256 differs from manifest")


def main() -> None:
    eps = episodes()
    for ep in eps:
        check_episode(ep)
    check_text_files()
    check_sizes()
    ids = [yaml.safe_load((e / "episode.yml").read_text())["id"] for e in eps]
    for dup in {i for i in ids if ids.count(i) > 1}:
        bad(f"episode id {dup} used twice")
    for line in problems:
        print("PROBLEM", line)
    print(f"validate_course: {len(eps)} episode(s), {len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
