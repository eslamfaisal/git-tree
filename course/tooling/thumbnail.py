#!/usr/bin/env python3
"""Renders an episode's YouTube thumbnails (1280x720 JPEG, under 1 MB) from <episode>/thumbnail/thumbnail.html.

    thumbnail.py <episode-dir>          writes <episode>/thumbnail/thumbnail.<lang>.jpg for en and ar
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenes  # noqa: E402

COURSE = HERE.parent


def main() -> None:
    from PIL import Image
    from playwright.sync_api import sync_playwright

    ep = Path(sys.argv[1]).resolve()
    html = (ep / "thumbnail" / "thumbnail.html").read_text()
    photo = (COURSE / "presenter" / "profile.jpg").as_uri()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=scenes.CHROME, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        for lang in ("en", "ar"):
            cfg = {"lang": lang, "d": 1, "presenter": None}
            inject = f'<link rel="stylesheet" href="{(scenes.KIT / "scene.css").as_uri()}"><script>window.__SCENE__={json.dumps(cfg)};</script><script src="{(scenes.KIT / "kit.js").as_uri()}"></script>'
            page_html = html.replace("<!--KIT-->", inject).replace("{{KIT}}", scenes.KIT.as_uri())
            tmp = ep / "thumbnail" / f".tmp-{lang}.html"
            tmp.write_text(page_html)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(tmp.as_uri())
            page.wait_for_timeout(400)
            png = page.screenshot(type="png")
            tmp.unlink()
            out = ep / "thumbnail" / f"thumbnail.{lang}.jpg"
            Image.open(io.BytesIO(png)).convert("RGB").save(out, quality=90, optimize=True)
            print(out, out.stat().st_size // 1024, "KB")
        browser.close()


if __name__ == "__main__":
    main()
