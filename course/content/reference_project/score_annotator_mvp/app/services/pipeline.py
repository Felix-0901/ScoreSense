from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import uuid

from app.config import ALLOWED_IMAGE_EXTENSIONS, ALLOWED_MUSICXML_EXTENSIONS, WORK_DIR, OUTPUT_DIR
from .converter import LabelMode
from .image_preprocessor import preprocess_score, PreprocessResult
from .musicxml import annotate_musicxml, save_note_report, AnnotatedNote
from .omr import run_oemer, OMRResult


@dataclass
class PipelineResult:
    job_id: str
    output_dir: Path
    annotated_musicxml: Path
    note_report: Path
    notes: list[AnnotatedNote]
    source_musicxml: Path
    preprocessed_image: Path | None = None
    binary_preview: Path | None = None
    omr_log: Path | None = None
    omr_backend: str | None = None


def process_file(
    input_path: str | Path,
    mode: LabelMode | str,
    *,
    preprocess: bool = True,
    show_accidental: bool = True,
    show_octave: bool = False,
    job_id: str | None = None,
) -> PipelineResult:
    input_path = Path(input_path)
    mode = LabelMode(mode)
    job_id = job_id or uuid.uuid4().hex[:12]

    work_dir = WORK_DIR / job_id
    output_dir = OUTPUT_DIR / job_id
    work_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    suffix = input_path.suffix.lower()
    preprocessed: PreprocessResult | None = None
    omr: OMRResult | None = None

    if suffix in ALLOWED_MUSICXML_EXTENSIONS:
        source_musicxml = work_dir / input_path.name
        shutil.copy2(input_path, source_musicxml)
    elif suffix in ALLOWED_IMAGE_EXTENSIONS:
        if preprocess:
            preprocessed = preprocess_score(input_path, work_dir)
            omr_input = preprocessed.enhanced_path
        else:
            omr_input = input_path
        omr_dir = work_dir / "omr"
        omr = run_oemer(omr_input, omr_dir)
        source_musicxml = omr.musicxml_path
    else:
        raise ValueError(
            f"Unsupported file extension {suffix!r}. "
            "Use PNG/JPG/etc. or XML/MusicXML/MXL."
        )

    annotated = output_dir / f"annotated_{mode.value}.musicxml"
    notes = annotate_musicxml(
        source_musicxml,
        annotated,
        mode,
        show_accidental=show_accidental,
        show_octave=show_octave,
    )
    note_report = output_dir / "notes.json"
    save_note_report(notes, note_report)

    return PipelineResult(
        job_id=job_id,
        output_dir=output_dir,
        annotated_musicxml=annotated,
        note_report=note_report,
        notes=notes,
        source_musicxml=source_musicxml,
        preprocessed_image=preprocessed.enhanced_path if preprocessed else None,
        binary_preview=preprocessed.binary_path if preprocessed else None,
        omr_log=omr.log_path if omr else None,
        omr_backend=omr.backend if omr else None,
    )
