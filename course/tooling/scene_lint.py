#!/usr/bin/env python3
"""Layout lint for scenes: text must never overlap other text, sit under a label or button, run out of its box
or leave the safe area. Checked in both languages at several moments of every scene, because things move.

    scene_lint.py scenes/*.html [--lang en --lang ar] [--seconds 20]

Exit code 1 when anything is found. compose.py runs it before rendering, so a broken layout cannot reach a video.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scenes  # noqa: E402

MOMENTS = (0.18, 0.35, 0.5, 0.65, 0.8, 0.98)
SAFE = 28  # px kept free at every edge

COLLECT = """
() => {
  const vis = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { o *= parseFloat(getComputedStyle(e).opacity); if (getComputedStyle(e).visibility === 'hidden') return 0; } return o; };
  const name = (el) => (el.className && typeof el.className === 'string' ? '.' + el.className.split(/\\s+/).filter(Boolean).slice(0, 2).join('.') : el.tagName.toLowerCase());
  const texts = [], pills = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    if (vis(el) < 0.35) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rects = [...r.getClientRects()].filter((q) => q.width > 1 && q.height > 1);
    if (!rects.length) continue;
    // Range rects are the font's content area (tall for Arabic faces); the glyphs fill the middle of it.
    const lines = rects.map((q) => ({ l: q.left, t: q.top + q.height * 0.16, r: q.right, b: q.bottom - q.height * 0.16 }));
    const box = { l: Math.min(...rects.map((q) => q.left)), t: Math.min(...rects.map((q) => q.top)), r: Math.max(...rects.map((q) => q.right)), b: Math.max(...rects.map((q) => q.bottom)) };
    // clipped by an overflow:hidden ancestor
    let clipped = null;
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflow === 'hidden' || cs.overflowX === 'hidden') { const q = e.getBoundingClientRect(); if (box.r > q.right + 1 || box.l < q.left - 1) clipped = name(e); break; }
    }
    texts.push({ el, box, lines, text: n.textContent.trim().slice(0, 40), cls: name(el), clipped });
  }
  for (const el of document.querySelectorAll('.lab, .chip, .btn, kbd, .presenter .who, .presenter .face, .tag, .brand')) {
    if (vis(el) < 0.35) continue;
    const q = el.getBoundingClientRect();
    if (q.width > 1) pills.push({ el, box: { l: q.left, t: q.top, r: q.right, b: q.bottom }, cls: name(el) });
  }
  return { texts: texts.map((x) => ({ ...x, el: undefined, owner: pills.findIndex((p) => p.el.contains(x.el)) })), pills: pills.map((p) => ({ box: p.box, cls: p.cls })) };
}
"""


def overlap(a: dict, b: dict) -> float:
    w = min(a["r"], b["r"]) - max(a["l"], b["l"])
    h = min(a["b"], b["b"]) - max(a["t"], b["t"])
    return max(0.0, w) * max(0.0, h)


def area(a: dict) -> float:
    return (a["r"] - a["l"]) * (a["b"] - a["t"])


def lint(html: Path, lang: str, seconds: float, presenter: dict | None) -> list[str]:
    from playwright.sync_api import sync_playwright

    problems: list[str] = []
    cfg = {"lang": lang, "d": seconds, "presenter": presenter}
    tmp = Path("/tmp") / f"lint-{html.stem}-{lang}.html"
    inject = (
        f'<link rel="stylesheet" href="{(scenes.KIT / "scene.css").as_uri()}">'
        f"<script>window.__SCENE__={json.dumps(cfg)};</script>"
        f'<script src="{(scenes.KIT / "kit.js").as_uri()}"></script>'
    )
    tmp.write_text(html.read_text().replace("<!--KIT-->", inject).replace("{{KIT}}", scenes.KIT.as_uri()))
    seen: set[str] = set()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=scenes.CHROME, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(tmp.as_uri())
        page.wait_for_timeout(250)
        for m in MOMENTS:
            page.evaluate("([t, v]) => window.__seek(t, v)", [m * seconds, 0.0])
            data = page.evaluate(COLLECT)
            texts, pills = data["texts"], data["pills"]
            tag = f"{html.name} [{lang}] t={m * seconds:.1f}s"

            def report(msg: str) -> None:
                if msg not in seen:
                    seen.add(msg)
                    problems.append(f"{tag}: {msg}")

            for i, a in enumerate(texts):
                b = a["box"]
                if b["l"] < SAFE or b["t"] < SAFE or b["r"] > 1920 - SAFE or b["b"] > 1080 - SAFE:
                    report(f"text leaves the safe area: {a['text']!r} ({a['cls']})")
                if a["clipped"]:
                    report(f"text clipped by {a['clipped']}: {a['text']!r}")
                for c in texts[i + 1:]:
                    if any(overlap(ra, rc) > 0.04 * min(area(ra), area(rc)) for ra in a["lines"] for rc in c["lines"]):
                        report(f"text overlaps text: {a['text']!r} ({a['cls']}) x {c['text']!r} ({c['cls']})")
                for pi, p in enumerate(pills):
                    if a["owner"] == pi:
                        continue
                    if any(overlap(ra, p["box"]) > 0.04 * area(ra) for ra in a["lines"]):
                        report(f"text sits under {p['cls']}: {a['text']!r} ({a['cls']})")
            for i, p in enumerate(pills):
                for q in pills[i + 1:]:
                    if overlap(p["box"], q["box"]) > 0.04 * min(area(p["box"]), area(q["box"])):
                        # a name plate belongs to its face; the face/plate pair is one thing
                        pair = {p["cls"], q["cls"]}
                        if pair == {".who", ".face"} or ".brand" in pair and len(pair) == 1:
                            continue
                        report(f"{p['cls']} overlaps {q['cls']}")
        browser.close()
    tmp.unlink(missing_ok=True)
    return problems


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes", nargs="+", type=Path)
    ap.add_argument("--lang", action="append", choices=["en", "ar"])
    ap.add_argument("--seconds", type=float, default=20.0)
    ns = ap.parse_args()
    presenter = {"name": "Eslam Faisal", "title": "Software Engineer & Instructor", "initials": "EF", "photo": None}
    bad: list[str] = []
    for html in ns.scenes:
        for lang in ns.lang or ["en", "ar"]:
            pres = dict(presenter)
            if lang == "ar":
                pres.update(name="إسلام فيصل", title="مهندس برمجيات ومحاضر")
            bad += lint(html, lang, ns.seconds, pres)
    for line in bad:
        print("LAYOUT", line)
    print(f"scene lint: {len(bad)} problem(s) in {len(ns.scenes)} scene(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
