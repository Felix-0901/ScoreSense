from __future__ import annotations

import argparse
from pathlib import Path
import sys

from app.services.converter import LabelMode


def cmd_web(args) -> int:
    try:
        import uvicorn
    except ImportError:
        print("Missing uvicorn. Run: pip install -r requirements.txt", file=sys.stderr)
        return 2
    uvicorn.run("app.web:app", host=args.host, port=args.port, reload=args.reload)
    return 0


def cmd_process(args) -> int:
    from app.services.pipeline import process_file
    result = process_file(
        args.input,
        args.mode,
        preprocess=not args.no_preprocess,
        show_accidental=not args.hide_accidental,
        show_octave=args.show_octave,
    )

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(result.annotated_musicxml.read_bytes())
        target = out
    else:
        target = result.annotated_musicxml

    print(f"Job: {result.job_id}")
    print(f"Notes: {len(result.notes)}")
    print(f"MusicXML: {target}")
    print(f"Note report: {result.note_report}")
    if result.preprocessed_image:
        print(f"Preprocessed: {result.preprocessed_image}")
    if result.omr_log:
        print(f"OMR log: {result.omr_log}")
    return 0


def cmd_preprocess(args) -> int:
    from app.services.image_preprocessor import preprocess_score
    result = preprocess_score(args.input, args.output_dir)
    print(f"Enhanced: {result.enhanced_path}")
    print(f"Binary preview: {result.binary_path}")
    print(f"Estimated rotation: {result.rotation_degrees:.2f} degrees")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="樂譜辨識與自動標註系統 MVP")
    sub = parser.add_subparsers(dest="command", required=True)

    p_web = sub.add_parser("web", help="Start the local web interface")
    p_web.add_argument("--host", default="127.0.0.1")
    p_web.add_argument("--port", type=int, default=8000)
    p_web.add_argument("--reload", action="store_true")
    p_web.set_defaults(func=cmd_web)

    p_process = sub.add_parser("process", help="Process an image or MusicXML file")
    p_process.add_argument("input")
    p_process.add_argument("--mode", choices=[m.value for m in LabelMode], default="solfege")
    p_process.add_argument("--output")
    p_process.add_argument("--no-preprocess", action="store_true")
    p_process.add_argument("--hide-accidental", action="store_true")
    p_process.add_argument("--show-octave", action="store_true")
    p_process.set_defaults(func=cmd_process)

    p_pre = sub.add_parser("preprocess", help="Only run image preprocessing")
    p_pre.add_argument("input")
    p_pre.add_argument("--output-dir", default="data/preprocess_demo")
    p_pre.set_defaults(func=cmd_preprocess)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
