#!/usr/bin/env python3
"""Renders one HTML scene (visuals/kit) to a lossless clip, frame by frame, deterministically.

    scenes.py --html scene.html --lang ar --seconds 14.2 --out scene.mkv [--fps 30] [--height 1080]
              [--presenter presenter.json] [--speak speak.json]

Every frame is a screenshot after seeking all CSS animations to that frame's time, so the result does not
depend on how fast the machine is. `--speak` is a JSON list of 0..1 voice levels, one per frame, that makes
the presenter's ring pulse with the voice.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "visuals" / "kit"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def render(html: Path, lang: str, seconds: float, out: Path, fps: int = 30, height: int = 1080, presenter: dict | None = None, speak: list[float] | None = None) -> int:
    from playwright.sync_api import sync_playwright

    frames = max(1, round(seconds * fps))
    scale = height / 1080
    page_src = html.read_text()
    tmp = out.with_suffix(".html")
    config = {"lang": lang, "d": round(frames / fps, 4), "presenter": presenter}
    inject = (
        f'<link rel="stylesheet" href="{(KIT / "scene.css").as_uri()}">'
        f"<script>window.__SCENE__={json.dumps(config)};</script>"
        f'<script src="{(KIT / "kit.js").as_uri()}"></script>'
    )
    tmp.write_text(page_src.replace("<!--KIT-->", inject).replace("{{KIT}}", KIT.as_uri()))
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "png", "-i", "-", "-c:v", "ffv1", "-level", "3", "-pix_fmt", "bgr0", str(out)],
        stdin=subprocess.PIPE,
    )
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=scale)
        page.goto(tmp.as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        for i in range(frames):
            level = speak[i] if speak and i < len(speak) else 0.0
            page.evaluate("([t, v]) => window.__seek(t, v)", [i / fps, level])
            enc.stdin.write(page.screenshot(type="png"))
        browser.close()
    enc.stdin.close()
    enc.wait()
    tmp.unlink(missing_ok=True)
    return frames


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, type=Path)
    ap.add_argument("--lang", required=True, choices=["en", "ar"])
    ap.add_argument("--seconds", required=True, type=float)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--presenter", type=Path)
    ap.add_argument("--speak", type=Path)
    ns = ap.parse_args()
    presenter = json.loads(ns.presenter.read_text()) if ns.presenter else None
    speak = json.loads(ns.speak.read_text()) if ns.speak else None
    n = render(ns.html, ns.lang, ns.seconds, ns.out, ns.fps, ns.height, presenter, speak)
    print(f"{ns.out.name}: {n} frames")


if __name__ == "__main__":
    main()
