# Tooling

| Script | What |
|---|---|
| `compose.py` | Builds one episode in one language: voice, scenes, app footage, captions, encode, quality gate. `--record` records the real-app journey. |
| `scenes.py` | Renders an HTML scene (`visuals/kit`) to frames, deterministically (seeked animations). |
| `scene_lint.py` | Layout lint for scenes: no text over text or over a label, nothing outside the safe area. `compose.py` runs it first. |
| `voice.py` | Voice-over: Piper en_US-ryan-high, per-sentence levelling, calibrated loudness. |
| `quality.py` | Delivery gate: 1080p or higher, 16:9, constant 30 fps, H.264 High, BT.709, AAC 48 kHz, -14 LUFS, true peak, no black frames. |
| `validate_course.py` | Schema, one-feature rule, English only, trademark terms, storage-tier and size rules. CI runs it. |
| `generate_index.py` | Rebuilds the table in `README.md` and `episodes.json`. `--check` in CI. |

## Requirements (Linux)

`ffmpeg` (libx264), Python 3.11 with `numpy pillow pyyaml playwright piper-tts pyloudnorm soundfile`, Chromium for
Playwright, fonts Inter and JetBrains Mono, and the app-recording stack of
`open-git-tree/scripts/demo` (Xvfb, `dbus-run-session`, `tauri-driver`, WebKitWebDriver, Node 24) with a built
`e2e` binary. Set `OGT_REPO` to the open-git-tree checkout. The scratch voices are fetched on first use.
