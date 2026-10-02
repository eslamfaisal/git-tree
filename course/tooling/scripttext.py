"""Script text helpers (no heavy dependencies): the {Shown|spoken} markup and sentence splitting."""
from __future__ import annotations

import re

SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")
MARKUP = re.compile(r"\{([^{}|]*)\|([^{}]*)\}")


def display_text(text: str) -> str:
    return MARKUP.sub(lambda m: m.group(1), text)


def spoken_text(text: str) -> str:
    return MARKUP.sub(lambda m: m.group(2), text)


def sentences(text: str) -> list[str]:
    """The beat's sentences, in the display form (captions): one synthesis call and one caption each.

    A fragment under three words ("Click it.") is joined to its neighbour: a one-line caption flashing by is hard to
    read anyway."""
    parts = [p.strip() for p in SENTENCE_END.split(" ".join(text.split()))]
    out: list[str] = []
    for p in (x for x in parts if x):
        if out and len(display_text(p).split()) < 3:
            out[-1] = f"{out[-1]} {p}"
        else:
            out.append(p)
    if len(out) > 1 and len(display_text(out[0]).split()) < 3:
        out[1] = f"{out[0]} {out[1]}"
        out.pop(0)
    return out
