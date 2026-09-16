from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable
import io
import json
import zipfile
import xml.etree.ElementTree as ET

from .converter import LabelMode, PitchInfo, pitch_to_label


@dataclass
class AnnotatedNote:
    index: int
    step: str
    alter: float
    octave: int | None
    label: str
    is_chord_tone: bool

    def to_dict(self) -> dict:
        return asdict(self)


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _namespace_prefix(tag: str) -> str:
    if tag.startswith("{"):
        return tag.split("}", 1)[0] + "}"
    return ""


def _child(element: ET.Element, name: str) -> ET.Element | None:
    for child in element:
        if _local_name(child.tag) == name:
            return child
    return None


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element if _local_name(child.tag) == name]


def _iter_by_local_name(root: ET.Element, name: str) -> Iterable[ET.Element]:
    for element in root.iter():
        if _local_name(element.tag) == name:
            yield element


def _read_mxl(path: Path) -> bytes:
    with zipfile.ZipFile(path, "r") as zf:
        target = None
        try:
            container = ET.fromstring(zf.read("META-INF/container.xml"))
            for element in container.iter():
                if _local_name(element.tag) == "rootfile":
                    target = element.attrib.get("full-path")
                    if target:
                        break
        except KeyError:
            pass

        if not target:
            candidates = [
                n for n in zf.namelist()
                if n.lower().endswith((".musicxml", ".xml")) and not n.startswith("META-INF/")
            ]
            if not candidates:
                raise ValueError("This MXL archive does not contain a MusicXML document.")
            target = candidates[0]
        return zf.read(target)


def load_tree(path: str | Path) -> ET.ElementTree:
    path = Path(path)
    if path.suffix.lower() == ".mxl":
        data = _read_mxl(path)
        return ET.ElementTree(ET.fromstring(data))
    return ET.parse(path)


def _extract_pitch(note: ET.Element) -> PitchInfo | None:
    if _child(note, "rest") is not None:
        return None
    pitch = _child(note, "pitch")
    if pitch is None:
        return None

    step_el = _child(pitch, "step")
    octave_el = _child(pitch, "octave")
    alter_el = _child(pitch, "alter")
    if step_el is None or not (step_el.text or "").strip():
        return None

    step = (step_el.text or "").strip().upper()
    alter = float((alter_el.text or "0").strip()) if alter_el is not None else 0.0
    octave = int((octave_el.text or "0").strip()) if octave_el is not None else None
    return PitchInfo(step=step, alter=alter, octave=octave)


def annotate_musicxml(
    input_path: str | Path,
    output_path: str | Path,
    mode: LabelMode | str,
    *,
    show_accidental: bool = True,
    show_octave: bool = False,
    lyric_number: str = "99",
) -> list[AnnotatedNote]:
    """Add generated labels as a dedicated MusicXML lyric line.

    Existing lyrics are preserved. Re-running the program replaces only lyric
    line number 99, so labels do not accumulate forever.
    """
    mode = LabelMode(mode)
    tree = load_tree(input_path)
    root = tree.getroot()
    namespace = _namespace_prefix(root.tag)

    results: list[AnnotatedNote] = []
    index = 0

    for note in _iter_by_local_name(root, "note"):
        pitch = _extract_pitch(note)
        if pitch is None:
            continue

        index += 1
        label = pitch_to_label(
            pitch,
            mode,
            show_accidental=show_accidental,
            show_octave=show_octave,
        )

        for lyric in list(_children(note, "lyric")):
            if lyric.attrib.get("number") == lyric_number:
                note.remove(lyric)

        lyric = ET.Element(f"{namespace}lyric", {"number": lyric_number, "color": "#C62828"})
        syllabic = ET.SubElement(lyric, f"{namespace}syllabic")
        syllabic.text = "single"
        text = ET.SubElement(lyric, f"{namespace}text")
        text.text = label
        note.append(lyric)

        results.append(
            AnnotatedNote(
                index=index,
                step=pitch.step,
                alter=pitch.alter,
                octave=pitch.octave,
                label=label,
                is_chord_tone=_child(note, "chord") is not None,
            )
        )

    if not results:
        raise ValueError("No pitched notes were found in the MusicXML file.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        pass
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return results


def save_note_report(notes: list[AnnotatedNote], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([n.to_dict() for n in notes], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
