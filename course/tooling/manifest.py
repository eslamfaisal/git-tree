#!/usr/bin/env python3
"""Writes assets/<series>/<id>-<slug>/manifest.json for an episode from its build output (.work/<id>/out).

    manifest.py <episode-dir>

Small files (captions, thumbnails) are copied into the assets folder (tier 1, plain git). Videos and the voice-over are
recorded in the manifest with size, sha256, quality-gate result and the command that regenerates them; they are
published to the repository separately (assets/README.md, "Publishing media").
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import yaml

COURSE = Path(__file__).resolve().parent.parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    meta = yaml.safe_load((ep / "episode.yml").read_text())
    name = f"{meta['id']}-{meta['slug']}"
    out = COURSE / ".work" / meta["id"] / "out"
    dest = COURSE / "assets" / meta["series"] / name
    files = []
    for src in sorted(out.glob(f"{name}.*")):
        if src.suffix in (".srt", ".vtt", ".jpg") or src.name.endswith((".chapters.txt", ".verification.md")):
            (dest / "video").mkdir(parents=True, exist_ok=True)
            target = dest / "video" / src.name
            shutil.copy2(src, target)
            files.append({"path": str(target.relative_to(dest)), "kind": "captions" if src.suffix in (".srt", ".vtt") else "chapters / verification", "tier": "git", "size": target.stat().st_size, "sha256": sha(target)})
        elif src.suffix in (".mp4", ".flac"):
            q = out / (src.stem + ".quality.json")
            entry = {"path": f"{'video' if src.suffix == '.mp4' else 'audio'}/{src.name}", "kind": "video" if src.suffix == ".mp4" else "voice-over",
                     "tier": "lfs (pending upload)", "size": src.stat().st_size, "sha256": sha(src),
                     "regenerate": f"python3 course/tooling/compose.py {ep.relative_to(COURSE.parent)} --height 1080"}
            if q.exists():
                entry["quality"] = {k: v for k, v in json.loads(q.read_text()).items() if k in ("width", "height", "fps", "codec", "duration_s", "lufs", "true_peak_db", "pass")}
            files.append(entry)
    thumb = ep / "thumbnail" / "thumbnail.jpg"
    if thumb.exists():
        (dest / "thumbnails").mkdir(parents=True, exist_ok=True)
        target = dest / "thumbnails" / thumb.name
        shutil.copy2(thumb, target)
        files.append({"path": str(target.relative_to(dest)), "kind": "thumbnail", "tier": "git", "size": target.stat().st_size, "sha256": sha(target)})
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "manifest.json").write_text(json.dumps({"episode": name, "recorded_against": meta.get("recorded_against"), "files": files}, indent=2, ensure_ascii=False) + "\n")
    print(f"{dest.relative_to(COURSE)}/manifest.json: {len(files)} files")


if __name__ == "__main__":
    main()
