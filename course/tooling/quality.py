#!/usr/bin/env python3
"""Per-video quality gate (rule 8): ffprobe + EBU R128 on a delivered MP4. Exit code 1 when a check fails.

    quality.py video.mp4 [--min-height 1080] [--fps 30]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def probe(path: Path) -> dict:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], text=True
    )
    return json.loads(out)


def loudness(path: Path) -> tuple[float, float]:
    """Integrated loudness (LUFS) and true peak (dBTP) of the audio track."""
    proc = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    summary = proc.stderr.split("Summary:")[-1]
    lufs = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    peak = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary).group(1))
    return lufs, peak


def black_seconds(path: Path) -> float:
    proc = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-an", "-vf", "blackdetect=d=0.5:pix_th=0.04", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return sum(float(m) for m in re.findall(r"black_duration:([\d.]+)", proc.stderr))


def check(path: Path, min_height: int = 1080, fps: float = 30.0) -> dict:
    info = probe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    duration = float(info["format"]["duration"])
    lufs, peak = loudness(path) if a else (None, None)
    frames = int(v.get("nb_frames") or 0)
    avg = v["avg_frame_rate"].split("/")
    measured_fps = float(avg[0]) / float(avg[1])
    result = {
        "file": path.name,
        "width": v["width"], "height": v["height"], "fps": round(measured_fps, 3), "codec": v["codec_name"],
        "profile": v.get("profile"), "pix_fmt": v["pix_fmt"],
        "color": [v.get("color_space"), v.get("color_primaries"), v.get("color_transfer")],
        "duration_s": round(duration, 2), "size_mb": round(int(info["format"]["size"]) / 1e6, 2),
        "audio": a["codec_name"] if a else None, "sample_rate": int(a["sample_rate"]) if a else None,
        "lufs": lufs, "true_peak_db": peak, "black_s": round(black_seconds(path), 2),
    }
    checks = {
        f"height >= {min_height}": v["height"] >= min_height,
        "16:9": abs(v["width"] / v["height"] - 16 / 9) < 0.01,
        f"{fps:g} fps constant": abs(measured_fps - fps) < 0.01 and v.get("r_frame_rate") == v["avg_frame_rate"],
        "H.264 High": v["codec_name"] == "h264" and v.get("profile") == "High",
        "yuv420p": v["pix_fmt"] == "yuv420p",
        "BT.709 tagged": result["color"] == ["bt709", "bt709", "bt709"],
        "frames match duration": frames == 0 or abs(frames / fps - float(v.get("duration", duration))) < 0.1,
        "audio AAC 48 kHz": bool(a) and a["codec_name"] == "aac" and int(a["sample_rate"]) == 48000,
        "loudness -14 +/- 1 LUFS": lufs is not None and abs(lufs + 14) <= 1.0,
        "true peak <= -1 dBTP": peak is not None and peak <= -0.9,
        "no black frames (> 0.5 s)": result["black_s"] == 0,
    }
    result["checks"] = checks
    result["pass"] = all(checks.values())
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--min-height", type=int, default=1080)
    ap.add_argument("--fps", type=float, default=30.0)
    ns = ap.parse_args()
    r = check(ns.video, ns.min_height, ns.fps)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if r["pass"] else 1)


if __name__ == "__main__":
    main()
