from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math

import cv2
import numpy as np


@dataclass
class PreprocessResult:
    enhanced_path: Path
    binary_path: Path
    rotation_degrees: float


def _read_image(path: Path) -> np.ndarray:
    raw = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def _write_image(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix or ".png"
    ok, buf = cv2.imencode(ext, image)
    if not ok:
        raise ValueError(f"Cannot encode image as {ext}")
    buf.tofile(str(path))


def _estimate_skew(binary_inv: np.ndarray) -> float:
    coords = np.column_stack(np.where(binary_inv > 0))
    if len(coords) < 100:
        return 0.0
    # np.where gives y,x; minAreaRect expects x,y-like points, but angle is
    # invariant for this use after normalization.
    angle = cv2.minAreaRect(coords.astype(np.float32))[-1]
    if angle < -45:
        angle = 90 + angle
    elif angle > 45:
        angle = angle - 90
    if abs(angle) > 15:
        return 0.0
    return float(angle)


def _rotate(image: np.ndarray, angle: float, border_value: int = 255) -> np.ndarray:
    if abs(angle) < 0.1:
        return image
    h, w = image.shape[:2]
    center = (w / 2.0, h / 2.0)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )


def preprocess_score(input_path: str | Path, output_dir: str | Path) -> PreprocessResult:
    """Create a conservative OMR-friendly score image plus a binary preview.

    The enhanced grayscale file is used for OMR. The binary file is mainly for
    teaching/debugging so students can see what thresholding does.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = _read_image(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve local contrast without destroying thin staff lines.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Estimate angle using an inverted Otsu mask.
    _, otsu_inv = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    angle = _estimate_skew(otsu_inv)
    enhanced = _rotate(enhanced, angle, border_value=255)

    # Gentle denoise then adaptive threshold for a diagnostic binary image.
    denoised = cv2.GaussianBlur(enhanced, (3, 3), 0)
    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )

    enhanced_path = output_dir / "preprocessed.png"
    binary_path = output_dir / "binary_preview.png"
    _write_image(enhanced_path, enhanced)
    _write_image(binary_path, binary)

    return PreprocessResult(
        enhanced_path=enhanced_path,
        binary_path=binary_path,
        rotation_degrees=angle,
    )
