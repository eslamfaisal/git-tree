# QA checklist (every episode)

**Accuracy**
- [ ] Every statement about GitTree matches the app: label, button, shortcut (verified in the app or `inventory.md`).
- [ ] Every git command was run in the demo repository at the episode's checkpoint and its output matches the screen.
- [ ] No feature that is not shipped; platform claims say which platform they were verified on.
- [ ] The recorded GitTree release is written in `episode.yml` (`recorded_against`).

**Picture**
- [ ] `scene_lint.py` passes: no text overlapping text, no label over a control, nothing outside the safe area.
- [ ] No text from the presenter, step label or boxes covers the app UI; no half-cut words at the zoom edges.
- [ ] Highlight boxes land on what the voice-over names, at the moment it is named.
- [ ] Readable at 1080p on a laptop screen; no flashing.

**Sound**
- [ ] Voice-over: loudness -14 LUFS, true peak under -1 dBTP; technical terms are pronounced as `glossary.md` says; no clipped or garbled sentence.
- [ ] Terms are pronounced as `glossary.md` says.

**Language**
- [ ] Captions match the voice word for word; the steps are in the order the screen shows them.

**Delivery**
- [ ] `quality.py` passes (1080p or higher, 30 fps constant, H.264 High, BT.709, AAC 48 kHz).
- [ ] Title, description, chapters, tags and thumbnail follow `seo/README.md`; no other product name.
- [ ] Files are in `assets/`, in the right storage tier, and `manifest.json` is current.
