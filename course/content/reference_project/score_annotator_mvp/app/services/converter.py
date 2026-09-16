from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LabelMode(str, Enum):
    SOLFEGE = "solfege"
    NUMBERED = "numbered"
    ZHUYIN = "zhuyin"


BASE_LABELS = {
    LabelMode.SOLFEGE: {
        "C": "Do", "D": "Re", "E": "Mi", "F": "Fa",
        "G": "Sol", "A": "La", "B": "Si",
    },
    LabelMode.NUMBERED: {
        "C": "1", "D": "2", "E": "3", "F": "4",
        "G": "5", "A": "6", "B": "7",
    },
    LabelMode.ZHUYIN: {
        "C": "ㄉㄛ", "D": "ㄖㄟ", "E": "ㄇㄧ", "F": "ㄈㄚ",
        "G": "ㄙㄛ", "A": "ㄌㄚ", "B": "ㄒㄧ",
    },
}


@dataclass(frozen=True)
class PitchInfo:
    step: str
    alter: float = 0
    octave: int | None = None


def _accidental_text(alter: float) -> str:
    rounded = round(alter * 2) / 2
    mapping = {
        -2.0: "♭♭",
        -1.5: "♭𝄲",
        -1.0: "♭",
        -0.5: "𝄲",
        0.0: "",
        0.5: "𝄳",
        1.0: "♯",
        1.5: "♯𝄳",
        2.0: "𝄪",
    }
    return mapping.get(rounded, f"({alter:+g})")


def _octave_text(octave: int | None) -> str:
    if octave is None or octave == 4:
        return ""
    if octave > 4:
        return "↑" * min(octave - 4, 3)
    return "↓" * min(4 - octave, 3)


def pitch_to_label(
    pitch: PitchInfo,
    mode: LabelMode | str,
    *,
    show_accidental: bool = True,
    show_octave: bool = False,
) -> str:
    """Convert a MusicXML pitch into the requested fixed-Do label.

    This MVP intentionally uses fixed-Do mapping:
    C -> Do / 1 / ㄉㄛ, D -> Re / 2 / ㄖㄟ ...
    """
    mode = LabelMode(mode)
    step = pitch.step.upper().strip()
    if step not in BASE_LABELS[mode]:
        raise ValueError(f"Unsupported pitch step: {pitch.step!r}")

    base = BASE_LABELS[mode][step]
    accidental = _accidental_text(pitch.alter) if show_accidental else ""
    octave = _octave_text(pitch.octave) if show_octave else ""

    if mode == LabelMode.NUMBERED:
        return f"{accidental}{base}{octave}"
    return f"{base}{accidental}{octave}"
