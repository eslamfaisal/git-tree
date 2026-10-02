"""Scratch voice-over for the course: Piper neural voices, sentence by sentence.

A scratch track exists to fix the timing of every beat and to review the script by ear. It is NOT the
published voice: a native speaker records that (see ../audio/README.md) and drops the takes in over it.

Voices (open licences, fetched once from the sherpa-onnx release mirror of Piper):
  en  en_US-ryan-high       ar  ar_JO-kareem-medium

Script markup: {Display|spoken} shows `Display` in captions and speaks `spoken`, so Arabic scripts can
keep Latin terms on screen ({commit|كوميت}) while the voice gets a phonetic spelling it can read.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import tarfile
import urllib.request
import wave
from dataclasses import dataclass
from pathlib import Path

RELEASE = "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models"
VOICES = {
    "en": ("vits-piper-en_US-ryan-high", "en_US-ryan-high.onnx"),
    "ar": ("vits-piper-ar_JO-kareem-medium", "ar_JO-kareem-medium.onnx"),
}
# Speaking rate of the scratch voices. The Arabic Piper voice reads slowly (about 1.5 words/s against 3.6 for English),
# so it is sped up to a natural lecture pace; a recorded voice-over replaces both (see compose.py).
RATE = {"en": 1.0, "ar": 1.55}
SENTENCE_END = re.compile(r"(?<=[.!?؟…])\s+")
MARKUP = re.compile(r"\{([^{}|]*)\|([^{}]*)\}")


def display_text(text: str) -> str:
    return MARKUP.sub(lambda m: m.group(1), text)


def spoken_text(text: str) -> str:
    return MARKUP.sub(lambda m: m.group(2), text)


def sentences(text: str) -> list[str]:
    """The beat's sentences, in the display form (captions) – one TTS call and one caption each."""
    parts = [p.strip() for p in SENTENCE_END.split(" ".join(text.split()))]
    return [p for p in parts if p]


def voice_dir(cache: Path, lang: str) -> Path:
    folder, _ = VOICES[lang]
    target = cache / "voices" / folder
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        archive = target.parent / f"{folder}.tar.bz2"
        print(f"fetching voice {folder} ...")
        urllib.request.urlretrieve(f"{RELEASE}/{folder}.tar.bz2", archive)
        with tarfile.open(archive) as tar:
            tar.extractall(target.parent)
        archive.unlink()
    return target


_loaded: dict[str, object] = {}


def _voice(cache: Path, lang: str):
    if lang not in _loaded:
        from piper import PiperVoice

        _, model = VOICES[lang]
        _loaded[lang] = PiperVoice.load(str(voice_dir(cache, lang) / model))
    return _loaded[lang]


@dataclass
class Clip:
    path: Path
    seconds: float
    text: str  # display form


def synth(cache: Path, lang: str, text: str, rate: float = 1.0) -> Clip:
    """One sentence -> a 22.05 kHz mono WAV in the cache (keyed by voice, rate and text)."""
    spoken = spoken_text(text)
    key = hashlib.sha256(f"{VOICES[lang][1]}|{rate}|{spoken}".encode()).hexdigest()[:20]
    path = cache / "vo" / f"{lang}-{key}.wav"
    if not path.exists():
        from piper import SynthesisConfig

        path.parent.mkdir(parents=True, exist_ok=True)
        voice = _voice(cache, lang)
        with wave.open(str(path), "wb") as wav:
            voice.synthesize_wav(spoken, wav, syn_config=SynthesisConfig(length_scale=1.0 / rate))
    with wave.open(str(path), "rb") as wav:
        seconds = wav.getnframes() / wav.getframerate()
    return Clip(path, seconds, display_text(text))


def loudness_gain_db(samples, rate: int, target: float = -14.0) -> float:
    import pyloudnorm as pyln

    meter = pyln.Meter(rate)
    return target - meter.integrated_loudness(samples)


def mux_audio(wav_in: Path, out: Path, target: float = -14.0, ceiling_db: float = -1.5) -> float:
    """Float WAV -> AAC 256 kbps at `target` LUFS integrated, true peak held under -1 dBTP.

    A gain and a limiter, calibrated against a measurement of the encoded file itself (two passes), because the
    limiter and the AAC encoder both move the level a little. Returns the measured loudness.
    """
    import quality

    gain = 0.0
    measured = target
    for _ in range(5):
        limit = 10 ** (ceiling_db / 20)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(wav_in), "-af", f"volume={gain:.2f}dB,alimiter=limit={limit:.3f}:level=disabled",
             "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(out)],
            check=True,
        )
        measured, peak = quality.loudness(out)
        if peak > -1.05:  # AAC can overshoot the limiter between samples: lower the ceiling and the gain follows
            ceiling_db -= 0.8
            continue
        if abs(measured - target) <= 0.3:
            break
        gain += target - measured
    return measured
