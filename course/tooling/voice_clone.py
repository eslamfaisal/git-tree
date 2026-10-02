"""Cloned narrator: ZipVoice zero-shot voice cloning (sherpa-onnx, CPU) and a speaker-similarity measure.

The reference is the author's own voice sample, kept at course/presenter/voice/ (gitignored, never committed).
Models come from the k2-fsa/sherpa-onnx GitHub release mirror and are cached under course/.work/models.

    voice_clone.py prepare              cut the prompt segment from the sample (needs voice/prompt.yml)
    voice_clone.py say "text" out.wav   one sentence in the cloned voice
    voice_clone.py score a.wav b.wav    speaker-embedding cosine similarity, 0..1 (same person is about 0.6 and up)
"""
from __future__ import annotations

import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf
import yaml

COURSE = Path(__file__).resolve().parent.parent
MODELS = COURSE / ".work" / "models"
VOICE = COURSE / "presenter" / "voice"
RELEASE = "https://github.com/k2-fsa/sherpa-onnx/releases/download"
ZIPVOICE = "sherpa-onnx-zipvoice-distill-int8-zh-en-emilia"
SPEAKER = "wespeaker_en_voxceleb_resnet34.onnx"
DENOISER = "gtcrn_simple.onnx"
VOCODER = "vocos_24khz.onnx"


def fetch() -> Path:
    MODELS.mkdir(parents=True, exist_ok=True)
    folder = MODELS / ZIPVOICE
    if not folder.exists():
        print("fetching ZipVoice ...")
        archive = MODELS / f"{ZIPVOICE}.tar.bz2"
        urllib.request.urlretrieve(f"{RELEASE}/tts-models/{ZIPVOICE}.tar.bz2", archive)
        with tarfile.open(archive) as tar:
            tar.extractall(MODELS)
        archive.unlink()
    for name, tag in ((VOCODER, "vocoder-models"), (SPEAKER, "speaker-recongition-models"), (DENOISER, "speech-enhancement-models")):
        if not (MODELS / name).exists():
            print(f"fetching {name} ...")
            urllib.request.urlretrieve(f"{RELEASE}/{tag}/{name}", MODELS / name)
    return folder


def denoise(src: Path, dst: Path) -> None:
    """Speech enhancement (GTCRN, sherpa-onnx) of a recording: the sample's room noise would otherwise be cloned along
    with the voice. Measured on the author's sample: noise floor 29 dB under the speech before, 59 dB after."""
    import sherpa_onnx

    fetch()
    x, sr = sf.read(str(src), dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    cfg = sherpa_onnx.OfflineSpeechDenoiserConfig(
        model=sherpa_onnx.OfflineSpeechDenoiserModelConfig(gtcrn=sherpa_onnx.OfflineSpeechDenoiserGtcrnModelConfig(model=str(MODELS / DENOISER)), num_threads=4)
    )
    out = sherpa_onnx.OfflineSpeechDenoiser(cfg).run(x.tolist(), sr)
    sf.write(str(dst), np.asarray(out.samples, dtype=np.float32), out.sample_rate)


def prepare() -> tuple[Path, str]:
    """The prompt: a clean 5 to 12 second stretch of the denoised sample at 24 kHz mono, level-normalised, and its exact words."""
    spec = yaml.safe_load((VOICE / "prompt.yml").read_text())
    clean = VOICE / "sample.denoised.wav"
    if not clean.exists() or clean.stat().st_mtime < (VOICE / spec["source"]).stat().st_mtime:
        wide = VOICE / "sample.48k.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VOICE / spec["source"]), "-ac", "1", "-ar", "48000", str(wide)], check=True)
        denoise(wide, clean)
        wide.unlink()
    out = VOICE / "prompt.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", str(spec["from"]), "-to", str(spec["to"]), "-i", str(clean), "-ac", "1", "-ar", "24000",
         "-af", "highpass=f=70,loudnorm=I=-20:TP=-2:LRA=7", str(out)],
        check=True,
    )
    return out, spec["text"]


_tts = None


def engine(num_threads: int = 4):
    global _tts
    if _tts is None:
        import sherpa_onnx

        folder = fetch()
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                zipvoice=sherpa_onnx.OfflineTtsZipvoiceModelConfig(
                    tokens=str(folder / "tokens.txt"), encoder=str(folder / "encoder.int8.onnx"), decoder=str(folder / "decoder.int8.onnx"),
                    vocoder=str(MODELS / VOCODER), data_dir=str(folder / "espeak-ng-data"), lexicon=str(folder / "lexicon.txt"),
                ),
                num_threads=num_threads,
            ),
        )
        _tts = sherpa_onnx.OfflineTts(cfg)
    return _tts


def say(text: str, out: Path, speed: float = 1.0, steps: int = 12) -> float:
    """Synthesises `text` in the cloned voice (sentence-level, fixed prompt) and writes a mono WAV; returns seconds."""
    prompt_wav, prompt_text = prepare() if not (VOICE / "prompt.wav").exists() else ((VOICE / "prompt.wav"), yaml.safe_load((VOICE / "prompt.yml").read_text())["text"])
    ref, sr = sf.read(str(prompt_wav), dtype="float32")
    audio = engine().generate(text, prompt_text, ref.tolist(), sr, speed=speed, num_steps=steps)
    samples = np.asarray(audio.samples, dtype=np.float32)
    sf.write(str(out), samples, audio.sample_rate)
    return len(samples) / audio.sample_rate


def embed(path: Path) -> np.ndarray:
    import sherpa_onnx

    fetch()
    cfg = sherpa_onnx.SpeakerEmbeddingExtractorConfig(model=str(MODELS / SPEAKER), num_threads=2)
    ex = sherpa_onnx.SpeakerEmbeddingExtractor(cfg)
    x, sr = sf.read(str(path), dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    s = ex.create_stream()
    s.accept_waveform(sr, x)
    s.input_finished()
    return np.asarray(ex.compute(s), dtype=np.float32)


def similarity(a: Path, b: Path) -> float:
    ea, eb = embed(a), embed(b)
    return float(np.dot(ea, eb) / (np.linalg.norm(ea) * np.linalg.norm(eb)))


def batch(jobs_file: Path) -> None:
    """Synthesises every job {text, out, speed} whose output does not exist yet, one file at a time.

    Meant to run in its own process: the native engine can crash on a rare input, and a crash must lose one sentence,
    not the whole episode (voice.prefetch restarts it, skipping what is done)."""
    import json

    for job in json.loads(jobs_file.read_text()):
        out = Path(job["out"])
        if not out.exists():
            say(job["text"], out, speed=job["speed"])
            print("done", out.name, flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prepare":
        print(prepare())
    elif cmd == "say":
        print(f"{say(sys.argv[2], Path(sys.argv[3])):.1f} s")
    elif cmd == "batch":
        batch(Path(sys.argv[2]))
    elif cmd == "score":
        print(f"{similarity(Path(sys.argv[2]), Path(sys.argv[3])):.3f}")
