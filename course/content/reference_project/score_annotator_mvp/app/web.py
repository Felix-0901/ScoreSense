from __future__ import annotations

from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR, UPLOAD_DIR, OUTPUT_DIR, WORK_DIR
from app.services.converter import LabelMode
from app.services.omr import OMRFailed, OMRUnavailable, find_oemer
from app.services.pipeline import process_file

app = FastAPI(title="樂譜辨識與自動標註系統", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "oemer_available": bool(find_oemer()),
        "supported_modes": [m.value for m in LabelMode],
    }


@app.post("/api/process")
async def process(
    file: UploadFile = File(...),
    mode: str = Form("solfege"),
    preprocess: bool = Form(True),
    show_accidental: bool = Form(True),
    show_octave: bool = Form(False),
):
    try:
        label_mode = LabelMode(mode)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown mode: {mode}")

    job_id = uuid.uuid4().hex[:12]
    original_name = Path(file.filename or "upload.bin").name
    upload_dir = UPLOAD_DIR / job_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    input_path = upload_dir / original_name

    with input_path.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    try:
        result = process_file(
            input_path,
            label_mode,
            preprocess=preprocess,
            show_accidental=show_accidental,
            show_octave=show_octave,
            job_id=job_id,
        )
    except OMRUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except OMRFailed as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}")

    payload = {
        "ok": True,
        "job_id": result.job_id,
        "mode": label_mode.value,
        "notes_count": len(result.notes),
        "notes_preview": [n.to_dict() for n in result.notes[:24]],
        "musicxml_url": f"/api/files/{result.job_id}/annotated_{label_mode.value}.musicxml",
        "notes_url": f"/api/files/{result.job_id}/notes.json",
        "omr_backend": result.omr_backend,
    }
    if result.preprocessed_image:
        payload["preprocessed_url"] = f"/api/work/{result.job_id}/preprocessed.png"
    if result.binary_preview:
        payload["binary_preview_url"] = f"/api/work/{result.job_id}/binary_preview.png"
    if result.omr_log:
        payload["omr_log_url"] = f"/api/work/{result.job_id}/omr/oemer.log"
    return payload


def _safe_file(base: Path, job_id: str, relative: str) -> Path:
    job_id = Path(job_id).name
    base_job = (base / job_id).resolve()
    target = (base_job / relative).resolve()
    if base_job not in target.parents and target != base_job:
        raise HTTPException(status_code=400, detail="Invalid path")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return target


@app.get("/api/files/{job_id}/{filename:path}")
def output_file(job_id: str, filename: str):
    return FileResponse(_safe_file(OUTPUT_DIR, job_id, filename), filename=Path(filename).name)


@app.get("/api/work/{job_id}/{filename:path}")
def work_file(job_id: str, filename: str):
    return FileResponse(_safe_file(WORK_DIR, job_id, filename), filename=Path(filename).name)
