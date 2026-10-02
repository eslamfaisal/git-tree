# Voice-over

The course is voiced by **native speakers**: English and Arabic. The scratch voices that `tooling/compose.py` generates
exist only to fix the timing and to review a script by ear. They are never published.

## Brief for the speakers

- Conversational and clear, like a patient colleague showing something on a shared screen. Not a news reader.
- One take per beat (`beats.yml`), in the order of the script, from the line after the beat's id. Leave half a second of
  silence at the start and one at the end. Re-record the whole beat for a mistake; do not splice inside a sentence.
- Say what the screen shows while it is shown: the picture is timed to your take, not the other way round.
- Read the commands as people say them: `git add -p` is "git add dash p".
- English: neutral international accent. Arabic: **Modern Standard Arabic in a light, spoken register** (no heavy
  formal constructions, no regional slang), so it reads naturally across the Arab world. The dialect decision is the
  owner's: change it here and in `glossary.md` if a regional dialect is preferred.
- Technical terms stay in English in the Arabic script (`commit`, `hunk`, `staging area`) and are pronounced the way
  Arabic-speaking developers say them. The pronunciation of each is fixed in `glossary.md`.

## Recording specification

| | |
|---|---|
| Format | WAV, 48 kHz, 24-bit, mono |
| Room | quiet, treated or soft furnishings; no fan or air conditioning running |
| Microphone | cardioid condenser or a good dynamic, 15 to 20 cm from the mouth, pop filter |
| Level | peaks around -6 dBFS; no limiter or noise reduction applied |
| Delivery | `assets/<series>/<id>-<slug>/audio/<lang>/<beat-id>.wav` |
| Loudness | the pipeline normalises the final mix to -14 LUFS integrated, true peak -1 dBTP |

## Review

Each Arabic script is read aloud and checked by a native speaker **before recording** (terms, phrasing, diacritics where
ambiguity is possible) and again against the recorded take. The review is logged in `qa/review-log.md`.

## Music and sound

None in the pilot. Any later music must carry a licence that allows monetised YouTube use; the licence file is stored
next to the track in `assets/shared/`.
