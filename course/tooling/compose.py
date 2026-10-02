#!/usr/bin/env python3
"""Builds one episode, in one language, from its beats.yml: voice-over, diagram scenes, app footage, captions.

    compose.py <episode-dir> --lang en|ar [--height 1080] [--take <dir>] [--out <dir>] [--burn]
    compose.py <episode-dir> --record          # records the app journey (needs the open-git-tree checkout)

A beat is one spoken passage over one picture. The picture is either an HTML scene (visuals/kit) or a span of
the recorded real-app take, whose speed is chosen so the footage lasts exactly as long as the voice. The same
take serves every language; only the voice, the on-screen text and the timing differ.

Environment: OGT_REPO = path of the open-git-tree checkout (default ../open-git-tree next to this repo).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
sys.path.insert(0, str(HERE))
import quality  # noqa: E402
import voice  # noqa: E402

FPS = 30
LEAD, TAIL, GAP = 0.45, 0.70, 0.28  # silence before the first sentence, after the last, between sentences (s)
MIN_SPEED, MAX_SPEED = 0.6, 3.2
OGT = Path(os.environ.get("OGT_REPO", COURSE.parent.parent / "open-git-tree")).resolve()
SIZES = {1080: (1920, 1080), 1440: (2560, 1440), 2160: (3840, 2160)}


def frames_of(seconds: float) -> int:
    return max(1, math.ceil(seconds * FPS - 1e-6))


def pick(spec, lang: str):
    """A value that may be given per language ({en:, ar:}) or once."""
    return spec[lang] if isinstance(spec, dict) and lang in spec else spec


def run(cmd: list[str], **kw) -> None:
    subprocess.run([str(c) for c in cmd], check=True, **kw)


# ───────────────────────────── plan ────────────────────────────────────────
class Beat:
    def __init__(self, raw: dict, lang: str, cache: Path, audio_dir: Path | None = None):
        self.raw, self.id = raw, raw["id"]
        self.kind = "scene" if "scene" in raw else "app"
        text = pick(raw["vo"], lang)
        recorded = audio_dir / lang / f"{self.id}.wav" if audio_dir else None
        if recorded and recorded.exists():  # a native speaker's take replaces the scratch voice for this beat
            import soundfile as sf

            info = sf.info(str(recorded))
            sents = voice.sentences(text)
            weights = [max(1, len(voice.display_text(x))) for x in sents]
            dur = info.frames / info.samplerate
            self.clips = [voice.Clip(recorded, dur * w / sum(weights), voice.display_text(x)) for x, w in zip(sents, weights)]
            self.recorded = recorded
        else:
            self.recorded = None
            self.clips = [voice.synth(cache, lang, s, rate=float(raw.get("rate", voice.RATE[lang]))) for s in voice.sentences(text)]
        speech = sum(c.seconds for c in self.clips) + GAP * (len(self.clips) - 1)
        self.seconds = max(LEAD + speech + TAIL, float(raw.get("min_sec", 0)))
        self.frames = frames_of(self.seconds)
        self.seconds = self.frames / FPS
        self.start = 0.0  # set by the timeline


def build_timeline(beats: list[Beat]) -> float:
    t = 0.0
    for b in beats:
        b.start = t
        t += b.seconds
    return t


# ───────────────────────────── audio ───────────────────────────────────────
def mix_voice(beats: list[Beat], total: float, out: Path) -> list[float]:
    """All sentences at their places -> 48 kHz mono float WAV at -14 LUFS; returns the per-frame voice level."""
    import soundfile as sf

    placed: list[tuple[Path, float]] = []
    for b in beats:
        t = b.start + LEAD
        if b.recorded:  # one take per beat, placed whole
            placed.append((b.recorded, t))
            continue
        for c in b.clips:
            placed.append((c.path, t))
            t += c.seconds + GAP
    cmd: list = ["ffmpeg", "-v", "error", "-y"]
    for path, _ in placed:
        cmd += ["-i", path]
    parts = [f"[{i}:a]aresample=48000,adelay={int(round(t * 1000))}[a{i}]" for i, (_, t) in enumerate(placed)]
    inputs = "".join(f"[a{i}]" for i in range(len(placed)))
    flt = ";".join(parts) + f";{inputs}amix=inputs={len(placed)}:normalize=0:duration=longest,apad=whole_dur={total:.3f}[m]"
    raw = out.with_suffix(".raw.wav")
    run(cmd + ["-filter_complex", flt, "-map", "[m]", "-ac", "1", "-c:a", "pcm_f32le", raw])
    data, rate = sf.read(str(raw), dtype="float32")
    gain_db = voice.loudness_gain_db(data, rate, -14.0)
    data = data * (10 ** (gain_db / 20))
    sf.write(str(out), data, rate, subtype="FLOAT")
    raw.unlink()
    hop = rate // FPS
    n = int(total * FPS) + 1
    rms = np.array([np.sqrt(np.mean(data[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(data) else 0.0 for i in range(n)])
    top = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1.0
    level, smooth = np.clip(rms / top, 0, 1), []
    prev = 0.0
    for v in level:
        prev = max(float(v), prev * 0.6)
        smooth.append(round(prev, 3))
    print(f"voice: {len(placed)} sentences, gain {gain_db:+.1f} dB")
    return smooth


# ───────────────────────────── scenes ──────────────────────────────────────
def render_scene(ep: Path, beat: Beat, lang: str, height: int, work: Path, presenter: dict, speak: list[float]) -> Path:
    html = ep / "scenes" / f"{beat.raw['scene']}.html"
    out = work / f"scene-{beat.id}.mkv"
    key = hashlib.sha256(
        json.dumps([html.read_text(), lang, beat.frames, height, presenter, [round(x, 2) for x in speak]], sort_keys=True).encode()
    ).hexdigest()[:16]
    stamp = out.with_suffix(".key")
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return out
    speak_file = work / f"speak-{beat.id}.json"
    speak_file.write_text(json.dumps(speak))
    pres_file = work / "presenter.json"
    pres_file.write_text(json.dumps(presenter))
    run([sys.executable, HERE / "scenes.py", "--html", html, "--lang", lang, "--seconds", f"{beat.frames / FPS:.4f}",
         "--out", out, "--height", height, "--presenter", pres_file, "--speak", speak_file])
    stamp.write_text(key)
    return out


# ───────────────────────────── app footage ─────────────────────────────────
def markers_of(take: Path) -> dict[str, float]:
    return {m["name"]: m["t"] for m in json.loads((take / "timeline.json").read_text())["markers"]}


def marker_time(markers: dict[str, float], ref: str) -> float:
    """A marker name, optionally followed by +/-seconds (marker names may contain '-': try the whole name first)."""
    if ref in markers:
        return markers[ref]
    for sign in "+-":
        name, _, off = ref.rpartition(sign)
        if name in markers:
            try:
                return markers[name] + (1 if sign == "+" else -1) * float(off)
            except ValueError:
                pass
    raise SystemExit(f"unknown marker {ref!r}; have {sorted(markers)}")


def storyboard(ep_beats: list[Beat], take: Path, lang: str, presenter: dict, speak: Path, height: int = 1080) -> dict:
    markers = markers_of(take)
    segments, camera, overlays = [], [], []
    warnings = []
    for b in ep_beats:
        app = b.raw["app"]
        a, z = app["from"], app["to"]
        length = marker_time(markers, z) - marker_time(markers, a)
        if length <= 0:
            raise SystemExit(f"beat {b.id}: 'to' ({z}) is not after 'from' ({a})")
        speed = length / b.seconds
        if speed < MIN_SPEED:
            lead_out = length / MIN_SPEED
            segments.append({"from": a, "to": z, "speed": MIN_SPEED})
            hold = b.seconds - lead_out
            segments.append({"from": z, "to": f"{z}+0.1", "speed": 0.1 / hold})  # hold the last picture
        else:
            segments.append({"from": a, "to": z, "speed": round(speed, 4)})
            if speed > MAX_SPEED:
                warnings.append(f"beat {b.id}: footage runs {speed:.1f}x; lengthen the voice or shorten the span")
        view = app.get("camera", "full")
        if isinstance(view, dict):
            view = dict(view)
        camera.append({"at": a, "view": view, "dur": float(app.get("camera_dur", 0.9))})
        for ov in b.raw.get("overlays", []):
            spec = {k: pick(v, lang) if k in ("text", "label") else v for k, v in ov.items()}
            spec.setdefault("from", a)
            spec.setdefault("to", z)
            overlays.append(spec)
    for w in warnings:
        print("WARNING", w)
    first, last = ep_beats[0].raw["app"]["from"], ep_beats[-1].raw["app"]["to"]
    photo = COURSE / "presenter" / presenter["photo_file"] if presenter.get("photo_file") else None
    overlays.append({"type": "presenter", "from": first, "to": last, "name": presenter["name"], "title": presenter["title"],
                     "initials": presenter["initials"], "photo": str(photo) if photo and photo.exists() else None, "speak": str(speak)})
    k = height / 1080  # the frame is laid out for 1920x1080 and scales with the output
    frame = {"x": round(208 * k), "y": round(24 * k), "w": round(1504 * k), "h": round(846 * k), "radius": round(18 * k)}
    return {"lang": lang, "loopDissolve": 0, "cursor": True, "frame": frame, "segments": segments, "camera": camera, "overlays": overlays}


def render_app(board: dict, take: Path, height: int, out: Path) -> None:
    w, h = SIZES[height]
    board_file = out.with_suffix(".json")
    board_file.write_text(json.dumps(board, indent=1, ensure_ascii=False))
    run([sys.executable, OGT / "scripts/demo/montage/render.py", "--take", take, "--storyboard", board_file, "--variant", "web",
         "--size", f"{w}x{h}", "--fps", FPS, "--out", out])


# ───────────────────────────── captions ────────────────────────────────────
def ts(t: float, comma: bool) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{',' if comma else '.'}{ms:03d}"


def write_captions(beats: list[Beat], stem: Path) -> list[tuple[float, float, str]]:
    cues = []
    for b in beats:
        t = b.start + LEAD
        for c in b.clips:
            cues.append((t, t + c.seconds, c.text))
            t += c.seconds + GAP
    stem.with_suffix(".srt").write_text("".join(f"{i}\n{ts(a, True)} --> {ts(z, True)}\n{x}\n\n" for i, (a, z, x) in enumerate(cues, 1)))
    stem.with_suffix(".vtt").write_text("WEBVTT\n\n" + "".join(f"{ts(a, False)} --> {ts(z, False)}\n{x}\n\n" for a, z, x in cues))
    return cues


# ───────────────────────────── main ────────────────────────────────────────
def load_presenter(lang: str) -> dict:
    p = yaml.safe_load((COURSE / "presenter" / "presenter.yml").read_text())
    photo = COURSE / "presenter" / p.get("photo", "")
    return {"name": pick(p["name"], lang), "title": pick(p["title"], lang), "initials": p["initials"], "photo_file": p.get("photo"),
            "photo": photo.as_uri() if photo.exists() and p.get("photo") else None}


def record(ep: Path, take: Path) -> None:
    meta = yaml.safe_load((ep / "episode.yml").read_text())
    cmd = ["bash", "-c", (
        f'cd "{OGT}/scripts/demo" && OGT_DEMO_WIDTH=1280 OGT_DEMO_HEIGHT=720 OGT_DEMO_SCALE=3 '
        f'dbus-run-session -- xvfb-run -a -s "-screen 0 3840x2160x24 -nolisten tcp" '
        f'node record.mjs {meta["journey"]} --journey "{ep / "journey.mjs"}" --repo-script "{COURSE / "demo-repo" / "build.sh"}" '
        f'--repo-arg {meta["checkpoint"]} --take 1 --work "{take.parent}" '
        '2> >(grep -v -E "xdg-desktop-portal|dbus-daemon|pw\\.conf|max threads|^$" >&2)')]
    run(cmd)
    src = take.parent / meta["journey"] / "take-1"
    if src != take:
        take.mkdir(parents=True, exist_ok=True)
        for f in ("raw.mkv", "timeline.json"):
            (take / f).write_bytes((src / f).read_bytes())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", type=Path)
    ap.add_argument("--lang", choices=["en", "ar"])
    ap.add_argument("--height", type=int, default=1080, choices=sorted(SIZES))
    ap.add_argument("--take", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--burn", action="store_true", help="also write a variant with the captions burned in")
    ns = ap.parse_args()

    ep = ns.episode.resolve()
    meta = yaml.safe_load((ep / "episode.yml").read_text())
    work_root = COURSE / ".work" / meta["id"]
    take = (ns.take or work_root / "take").resolve()
    if ns.record:
        record(ep, take)
        return
    if not ns.lang:
        raise SystemExit("--lang is required")
    lang = ns.lang
    work = work_root / lang / str(ns.height)
    work.mkdir(parents=True, exist_ok=True)
    cache = COURSE / ".work" / "cache"
    plan = yaml.safe_load((ep / "beats.yml").read_text())
    audio_dir = COURSE / "assets" / meta["series"] / f"{meta['id']}-{meta['slug']}" / "audio"
    beats = [Beat(r, lang, cache, audio_dir) for r in plan["beats"]]
    total = build_timeline(beats)
    print(f"{meta['id']} [{lang}] {len(beats)} beats, {total:.1f} s")

    import scene_lint

    scene_files = sorted({ep / "scenes" / f"{b.raw['scene']}.html" for b in beats if b.kind == "scene"})
    problems = [p for f in scene_files for p in scene_lint.lint(f, lang, 20.0, {"name": "x", "title": "y", "initials": "EF", "photo": None})]
    if problems:
        raise SystemExit("scene layout problems (fix before rendering):\n  " + "\n  ".join(problems))

    wav = work / "voice.wav"
    speak = mix_voice(beats, total, wav)
    presenter = load_presenter(lang)

    # contiguous runs of the same kind of beat become one clip
    runs: list[list[Beat]] = []
    for b in beats:
        if runs and runs[-1][0].kind == "app" and b.kind == "app":
            runs[-1].append(b)
        else:
            runs.append([b])

    def level(b: Beat, n: int) -> list[float]:
        i = int(round(b.start * FPS))
        return speak[i:i + n]

    jobs = []
    for r in runs:
        first = r[0]
        if first.kind == "scene":
            jobs.append((r, lambda b=first: render_scene(ep, b, lang, ns.height, work, presenter, level(b, b.frames))))
        else:
            def app_job(r=r):
                n = sum(b.frames for b in r)
                sp = work / f"speak-{r[0].id}.json"
                sp.write_text(json.dumps(level(r[0], n)))
                out = work / f"app-{r[0].id}.mkv"
                render_app(storyboard(r, take, lang, presenter, sp, ns.height), take, ns.height, out)
                return out
            jobs.append((r, app_job))
    # scenes render in parallel (each is its own browser); the single app render streams the 4K capture
    with ThreadPoolExecutor(max_workers=3) as pool:
        clips = [f.result() for f in [pool.submit(j) for _, j in jobs]]

    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{c}'\n" for c in clips))
    out_dir = (ns.out or work_root / "out").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / f"{meta['id']}-{meta['slug']}.{lang}.{ns.height}p"
    cues = write_captions(beats, stem)

    aac = work / "voice.m4a"
    voice.mux_audio(wav, aac)
    w, h = SIZES[ns.height]
    crf = {1080: 17, 1440: 17, 2160: 18}[ns.height]
    vf = f"scale={w}:{h}:flags=lanczos:out_color_matrix=bt709:out_range=tv,format=yuv420p"
    enc = ["-c:v", "libx264", "-preset", "slow", "-crf", crf, "-profile:v", "high", "-level", "5.1" if ns.height == 2160 else "4.2",
           "-r", FPS, "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
           "-c:a", "copy", "-movflags", "+faststart", "-shortest"]
    mp4 = stem.with_suffix(".mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat, "-i", aac, "-vf", vf, *enc, mp4])
    if ns.burn:
        font = "Noto Sans Arabic" if lang == "ar" else "Inter"
        style = f"FontName={font},FontSize={int(h * 0.036)},PrimaryColour=&HFFFFFF&,OutlineColour=&H101010&,BorderStyle=3,Outline=1,Shadow=0,MarginV={int(h * 0.075)}"
        burned = stem.with_name(stem.name + ".captioned").with_suffix(".mp4")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat, "-i", aac,
             "-vf", f"{vf},subtitles={stem.with_suffix('.srt')}:force_style='{style}'", *enc, burned])
    import soundfile as sf
    data, rate = sf.read(str(wav), dtype="float32")
    flac = stem.with_suffix(".voice.flac")
    sf.write(str(flac), data, rate, format="FLAC", subtype="PCM_24")
    result = quality.check(mp4, 1080, FPS)
    (stem.with_suffix(".quality.json")).write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({k: result[k] for k in ("width", "height", "duration_s", "size_mb", "lufs", "true_peak_db", "pass")}))
    for name, ok in result["checks"].items():
        print(("  ok   " if ok else "  FAIL ") + name)
    print(f"wrote {mp4}")
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
