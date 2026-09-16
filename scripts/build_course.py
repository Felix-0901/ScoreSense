#!/usr/bin/env python3
"""Build the public static ScoreSense curriculum from its checked-in sources.

The source handouts live in ``course/content``.  Teacher-only material is kept
in ``course/private`` and is deliberately outside every public output tree.
Run this script from any directory with:

    python scripts/build_course.py

It produces ``course/site/lessons.json``, copied practice materials, and three
download archives.  The build never reads the original Downloads folder, so a
fresh checkout can reproduce the public artefacts after installing
``requirements-course.txt``.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "course" / "content"
SITE_DIR = ROOT / "course" / "site"
LESSONS_JSON = SITE_DIR / "lessons.json"

ADMONITION_RE = re.compile(r"^:::(info|warning|tip)\s*$", re.MULTILINE)
PUBLIC_IDS = tuple(f"{number:02d}" for number in range(27)) + ("B", "C", "D", "readme")


@dataclass(frozen=True)
class LessonSource:
    identifier: str
    path: Path


class PlainTextExtractor(HTMLParser):
    """Small dependency-free HTML-to-text conversion for the JSON search text."""

    BLOCK_TAGS = {"p", "div", "aside", "section", "article", "li", "tr", "pre", "br"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "".join(self.parts)).strip()


def lesson_sources() -> list[LessonSource]:
    """Return the exact public lesson sequence, excluding the teacher edition."""
    by_id: dict[str, Path] = {}
    for path in CONTENT_DIR.glob("*.md"):
        filename = path.name
        chapter = re.match(r"^(\d\d)_", filename)
        if chapter:
            by_id[chapter.group(1)] = path
        elif filename.startswith("B_"):
            by_id["B"] = path
        elif filename.startswith("C_"):
            by_id["C"] = path
        elif filename.startswith("D_"):
            by_id["D"] = path
        elif filename == "README_先看這份.md":
            by_id["readme"] = path

    missing = [identifier for identifier in PUBLIC_IDS if identifier not in by_id]
    if missing:
        raise FileNotFoundError(f"Missing public lesson sources: {', '.join(missing)}")
    return [LessonSource(identifier, by_id[identifier]) for identifier in PUBLIC_IDS]


def normalize_hackmd(source: str) -> str:
    """Convert HackMD-only syntax outside fenced code blocks.

    A lesson about HackMD deliberately includes literal ``[TOC]`` and
    ``:::info`` examples.  Those examples are teaching content, so only real
    document syntax is normalized.
    """
    normalized: list[str] = []
    fence: tuple[str, int] | None = None
    for line in source.splitlines(keepends=True):
        fence_match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            normalized.append(line)
            continue
        if fence is not None:
            normalized.append(line)
            continue

        if re.fullmatch(r"\[TOC\]\s*(?:\n)?", line):
            continue
        opening = ADMONITION_RE.fullmatch(line.rstrip("\r\n"))
        if opening:
            normalized.append(f'<aside class="admonition {opening.group(1)}" markdown="1">\n')
        elif re.fullmatch(r":::\s*(?:\r?\n)?", line):
            normalized.append("</aside>\n")
        else:
            normalized.append(line)
    return "".join(normalized)


def source_title(source: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", source)
    return match.group(1).strip() if match else fallback


def flatten_toc(tokens: list[dict[str, object]]) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    for token in tokens:
        sections.append(
            {
                "id": str(token["id"]),
                "title": str(token["name"]),
                "level": int(token["level"]),
            }
        )
        children = token.get("children", [])
        if isinstance(children, list):
            sections.extend(flatten_toc(children))
    return sections


def html_to_text(rendered_html: str) -> str:
    parser = PlainTextExtractor()
    parser.feed(rendered_html)
    parser.close()
    return html.unescape(parser.text())


def render_lesson(item: LessonSource) -> dict[str, object]:
    source = item.path.read_text(encoding="utf-8")
    compiler = markdown.Markdown(
        extensions=["extra", "nl2br", "toc", "md_in_html"],
        extension_configs={"toc": {"permalink": False}},
    )
    rendered_html = compiler.convert(normalize_hackmd(source))
    # Keep the H1 in the rendered article so each deep-linked lesson remains
    # meaningful when it is opened without surrounding application chrome.
    return {
        "id": item.identifier,
        "title": source_title(source, item.path.stem),
        "html": rendered_html,
        "text": html_to_text(rendered_html),
        "sections": flatten_toc(compiler.toc_tokens),
    }


def copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def add_zip_member(bundle: zipfile.ZipFile, path: Path, member_name: Path) -> None:
    """Write one regular file with fixed metadata for reproducible archives."""
    info = zipfile.ZipInfo(member_name.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    bundle.writestr(info, path.read_bytes())


def write_zip(archive: Path, source: Path, root_name: str) -> None:
    """Create a deterministic public archive from a single audited source tree."""
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(source.rglob("*")):
            if path.is_symlink() or not path.is_file() or path.name == ".DS_Store":
                continue
            relative = path.relative_to(source)
            add_zip_member(bundle, path, Path(root_name) / relative)


def build_downloads() -> None:
    downloads = SITE_DIR / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)

    # Public source archive is deliberately constructed from course/content,
    # which contains all student material but never course/private/teacher A.
    public_sources = downloads / "ScoreSense_逐步專題講義_v2_學生版.zip"
    with zipfile.ZipFile(public_sources, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(CONTENT_DIR.rglob("*")):
            if not path.is_symlink() and path.is_file() and path.name != ".DS_Store":
                add_zip_member(
                    bundle,
                    path,
                    Path("ScoreSense_逐步專題講義_v2") / path.relative_to(CONTENT_DIR),
                )

    write_zip(downloads / "materials.zip", CONTENT_DIR / "materials", "materials")
    write_zip(
        downloads / "reference-project.zip",
        CONTENT_DIR / "reference_project" / "score_annotator_mvp",
        "score_annotator_mvp",
    )


def main() -> None:
    if not CONTENT_DIR.is_dir():
        raise FileNotFoundError(f"Course source directory is missing: {CONTENT_DIR}")

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    copy_tree(CONTENT_DIR / "materials", SITE_DIR / "materials")
    lessons = [render_lesson(item) for item in lesson_sources()]
    LESSONS_JSON.write_text(
        json.dumps(lessons, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    build_downloads()
    print(f"Built {len(lessons)} public lessons: {LESSONS_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
