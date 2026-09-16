from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import subprocess
import sys


@dataclass
class OMRResult:
    musicxml_path: Path
    log_path: Path
    backend: str


class OMRUnavailable(RuntimeError):
    pass


class OMRFailed(RuntimeError):
    pass


def find_oemer() -> str | None:
    explicit = os.environ.get("OEMER_COMMAND")
    if explicit:
        return explicit
    local = Path(sys.executable).parent / ("oemer.exe" if os.name == "nt" else "oemer")
    if local.is_file():
        return str(local)
    return shutil.which("oemer")


def _find_musicxml(directory: Path) -> Path | None:
    candidates = []
    for pattern in ("*.musicxml", "*.mxl", "*.xml"):
        candidates.extend(directory.glob(pattern))
    candidates = [p for p in candidates if p.name.lower() != "container.xml"]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def run_oemer(image_path: str | Path, output_dir: str | Path, timeout: int = 1800) -> OMRResult:
    command = find_oemer()
    if not command:
        raise OMRUnavailable(
            "oemer command was not found. Install the optional OMR dependency "
            "or set OEMER_COMMAND to the full executable path."
        )

    image_path = Path(image_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "oemer.log"

    attempts = [
        [command, str(image_path)],
        [command, "-d", str(image_path)],  # official troubleshooting fallback
    ]
    all_logs: list[str] = []

    for attempt_no, args in enumerate(attempts, start=1):
        try:
            completed = subprocess.run(
                args,
                cwd=output_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            all_logs.append(f"Attempt {attempt_no}: timeout after {timeout}s\n{exc}\n")
            continue

        all_logs.append(
            f"=== Attempt {attempt_no} ===\n"
            f"Command: {' '.join(args)}\n"
            f"Return code: {completed.returncode}\n"
            f"--- stdout ---\n{completed.stdout}\n"
            f"--- stderr ---\n{completed.stderr}\n"
        )
        result = _find_musicxml(output_dir)
        if completed.returncode == 0 and result is not None:
            log_path.write_text("\n".join(all_logs), encoding="utf-8")
            return OMRResult(result, log_path, "oemer")

    log_path.write_text("\n".join(all_logs), encoding="utf-8")
    raise OMRFailed(
        f"oemer failed to produce MusicXML. See log: {log_path}. "
        "The second attempt automatically disabled oemer's own deskew step."
    )
