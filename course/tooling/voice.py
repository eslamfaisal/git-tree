"""Voice-over for the course (English).

Backends:
  clone  the author's own voice, cloned from a sample with ZipVoice (voice_clone.py). Default when
         presenter/voice/prompt.wav exists.
  piper  a neural scratch voice (Piper en_US-ryan), the fallback when no sample is present.

A narrator's real recording of a beat always wins: see compose.py ("audio/<beat-id>.wav").

Script markup: {Display|spoken} shows `Display` in captions and speaks `spoken`, so technical terms can be respelled
for the voice ({git add -p|git add dash p}) while the captions keep the real text.
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

import numpy as np
import soundfile as sf
from scripttext import display_text, sentences, spoken_text  # noqa: F401  (re-exported)

COURSE = Path(__file__).resolve().parent.parent
PIPER_RELEASE = "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models"
PIPER_VOICE = ("vits-piper-en_US-ryan-high", "en_US-ryan-high.onnx")
TARGET_RMS_DB = -20.0  # every sentence is levelled to this RMS before mixing, so the delivery is even


def backend() -> str:
    return "clone" if (COURSE / "presenter" / "voice" / "prompt.wav").exists() else "piper"


def _prompt_fingerprint() -> str:
    folder = COURSE / "presenter" / "voice"
    h = hashlib.sha256()
    for name in ("prompt.wav", "prompt.yml"):
        h.update((folder / name).read_bytes())
    return h.hexdigest()[:10]


@dataclass
class Clip:
    path: Path
    seconds: float
    text: str  # display form


def _level(samples: np.ndarray, sr: int) -> np.ndarray:
    """Trim leading and trailing silence, level to TARGET_RMS_DB (RMS of the active parts), keep peaks under -1 dBFS."""
    if len(samples) == 0:
        return samples
    frame = max(1, sr // 100)
    n = len(samples) // frame
    rms = np.sqrt(np.mean(samples[: n * frame].reshape(n, frame) ** 2, axis=1))
    active = np.where(rms > max(rms.max() * 0.04, 1e-4))[0]
    if len(active):
        a, b = max(0, active[0] - 3) * frame, min(n, active[-1] + 6) * frame
        samples = samples[a:b]
        rms = rms[active]
    gain = (10 ** (TARGET_RMS_DB / 20)) / max(float(np.sqrt(np.mean(rms ** 2))), 1e-6)
    out = samples * gain
    peak = float(np.max(np.abs(out)))
    return out * (0.89 / peak) if peak > 0.89 else out


def _piper(text: str, out: Path, rate: float) -> None:
    folder, model = PIPER_VOICE
    target = COURSE / ".work" / "voices" / folder
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        archive = target.parent / f"{folder}.tar.bz2"
        urllib.request.urlretrieve(f"{PIPER_RELEASE}/{folder}.tar.bz2", archive)
        with tarfile.open(archive) as tar:
            tar.extractall(target.parent)
        archive.unlink()
    from piper import PiperVoice, SynthesisConfig

    voice = PiperVoice.load(str(target / model))
    with wave.open(str(out), "wb") as wav:
        voice.synthesize_wav(text, wav, syn_config=SynthesisConfig(length_scale=1.0 / rate))


# Speaking speed per backend. The cloned voice, like its sample, speaks unhurriedly; a lecture needs a little more pace.
DEFAULT_RATE = {"clone": 1.12, "piper": 1.0}


def _key(which: str, spoken: str, rate: float) -> str:
    return hashlib.sha256(f"{which}|{_prompt_fingerprint() if which == 'clone' else PIPER_VOICE[1]}|{rate}|{spoken}".encode()).hexdigest()[:20]


def prefetch(cache: Path, items: list[tuple[str, float | None]]) -> None:
    """Generates the raw takes of every sentence not yet cached, in a separate process that is restarted if the native
    engine crashes."""
    if backend() != "clone":
        return
    import json
    import sys

    jobs = []
    for text, rate in items:
        spoken = spoken_text(text)
        r = DEFAULT_RATE["clone"] if rate is None else rate
        final = cache / "vo" / f"clone-{_key('clone', spoken, r)}.wav"
        raw = final.with_suffix(".raw.wav")
        if not final.exists() and not raw.exists():
            jobs.append({"text": spoken, "out": str(raw), "speed": 1.0})  # speeds above 1.05 crash the engine on some inputs: stretch afterwards
    if not jobs:
        return
    (cache / "vo").mkdir(parents=True, exist_ok=True)
    jobs_file = cache / "vo" / "jobs.json"
    for attempt in range(len(jobs) + 3):
        pending = [j for j in jobs if not Path(j["out"]).exists()]
        if not pending:
            return
        jobs_file.write_text(json.dumps(pending))
        proc = subprocess.run([sys.executable, str(Path(__file__).with_name("voice_clone.py")), "batch", str(jobs_file)], capture_output=True, text=True)
        if proc.returncode != 0:
            first = next(j for j in pending if not Path(j["out"]).exists())
            print(f"voice engine stopped on: {first['text'][:60]!r} (attempt {attempt + 1})")
    raise SystemExit("voice synthesis kept failing; see the sentences above")


def synth(cache: Path, text: str, rate: float | None = None) -> Clip:
    """One sentence -> a mono WAV in the cache, keyed by backend, voice, speed and the spoken words."""
    spoken = spoken_text(text)
    which = backend()
    rate = DEFAULT_RATE[which] if rate is None else rate
    path = cache / "vo" / f"{which}-{_key(which, spoken, rate)}.wav"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = path.with_suffix(".raw.wav")
        if not raw.exists():
            if which == "clone":
                import voice_clone

                voice_clone.say(spoken, raw, speed=1.0)
            else:
                _piper(spoken, raw, rate)
        if which == "clone" and abs(rate - 1.0) > 1e-3:  # pitch-preserving time stretch (the engine's own speed option can crash)
            stretched = raw.with_suffix(".stretch.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", f"atempo={rate}", str(stretched)], check=True)
            stretched.replace(raw)
        x, sr = sf.read(str(raw), dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        sf.write(str(path), _level(x, sr), sr)
        raw.unlink()
    info = sf.info(str(path))
    return Clip(path, info.frames / info.samplerate, display_text(text))


def loudness_gain_db(samples, rate: int, target: float = -14.0) -> float:
    import pyloudnorm as pyln

    return target - pyln.Meter(rate).integrated_loudness(samples)


def mux_audio(wav_in: Path, out: Path, target: float = -14.0, ceiling_db: float = -1.5) -> float:
    """Float WAV -> AAC 256 kbps at `target` LUFS integrated, true peak held under -1 dBTP.

    A gain and a limiter, calibrated against a measurement of the encoded file itself, because the limiter and the AAC
    encoder both move the level a little. Returns the measured loudness.
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
