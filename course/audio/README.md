# Voice-over

The course is narrated in **English, in the author's own voice**. The voice is cloned from a recording sample with
ZipVoice (`tooling/voice_clone.py`, runs on CPU) and every sentence is generated from the script.

## How the voice is made

1. The author's sample (30 to 60 seconds, quiet room, natural pace) lives in `presenter/voice/` and is **never
   committed**: the folder is gitignored.
2. `presenter/voice/prompt.yml` names the clean 5 to 12 second stretch used as the voice prompt and the exact words in it.
3. `tooling/voice.py` synthesises the script sentence by sentence (a cache keyed by voice, speed and text means an edit
   only re-synthesises what changed), levels each sentence, and `compose.py` mixes them to -14 LUFS with true peak under
   -1 dBTP.
4. Speaker similarity to the sample is measured with a speaker-embedding model (`voice_clone.py score a.wav b.wav`).
   Two parts of the author's own recording score 0.86; the cloned voice scores 0.71 against the whole sample.

## A real recording always wins

To replace the generated voice for a beat, record it and save it as
`assets/<series>/<id>-<slug>/audio/<beat-id>.wav` (WAV, 48 kHz, 24-bit, mono, peaks around -6 dBFS, quiet room,
a half second of silence at each end). `compose.py` uses it for that beat and the generated voice for the rest.

## Disclosure

The narrator is a synthetic voice made from the author's own voice with the author's consent. Every upload sets
YouTube's *altered or synthetic content* option and the description says so (`seo/README.md`).

## Music and sound

None. Any later music must carry a licence that allows monetised use; the licence file is stored next to the track in
`assets/shared/`.
