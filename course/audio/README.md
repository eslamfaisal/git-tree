# Voice-over

The course is narrated in **English** by a clean neural text-to-speech voice: **Piper `en_US-ryan-high`**. Every
sentence of every script is generated from the text, so a script edit never needs a recording session.

## How the voice is made

1. `tooling/voice.py` splits each beat into sentences (a fragment under three words is joined to its neighbour) and
   synthesises them one by one. A cache keyed by voice, speed and text means an edit only re-synthesises what changed.
2. Each sentence is trimmed and levelled to the same RMS, so the delivery is even.
3. `tooling/compose.py` places the sentences on the timeline and mixes them; the final stage sets -14 LUFS integrated
   with the true peak under -1 dBTP (calibrated against a measurement of the encoded file).

## Pronunciation

Technical terms are respelled in the script with `{Shown|spoken}` markup: captions show the real text, the voice reads
the respelling. The lexicon is `../glossary.md`; add a row whenever a term is mispronounced.

## A real recording always wins

To replace the generated voice for a beat, record it and save it as
`assets/<series>/<id>-<slug>/audio/<beat-id>.wav` (WAV, 48 kHz, 24-bit, mono, peaks around -6 dBFS, quiet room, half a
second of silence at each end). `compose.py` uses it for that beat and the generated voice for the rest.

## Disclosure

The narration is synthetic. Every upload turns on YouTube's *altered or synthetic content* option and the description
says so (`../seo/README.md`).

## Music and sound

None. Any later music must carry a licence that allows monetised use; the licence file is stored next to the track in
`assets/shared/`.
