"""Regression checks for the public ScoreSense curriculum build."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
import zipfile
from pathlib import Path


try:
    import markdown
except ImportError:
    raise unittest.SkipTest("Install requirements-course.txt to run classroom build tests")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_course.py"
SPEC = importlib.util.spec_from_file_location("build_course", SCRIPT_PATH)
assert SPEC and SPEC.loader
build_course = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_course
SPEC.loader.exec_module(build_course)


class CourseBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build_course.main()
        cls.site = ROOT / "course" / "site"
        cls.lessons = json.loads((cls.site / "lessons.json").read_text(encoding="utf-8"))

    def test_public_lesson_contract_has_31_chapters(self) -> None:
        expected_ids = [f"{number:02d}" for number in range(27)] + ["B", "C", "D", "readme"]
        self.assertEqual([lesson["id"] for lesson in self.lessons], expected_ids)
        for lesson in self.lessons:
            self.assertEqual(set(lesson), {"id", "title", "html", "text", "sections"})
            self.assertIn("<h1", lesson["html"])
            self.assertTrue(lesson["sections"])
            self.assertTrue(all(section["id"] in lesson["html"] for section in lesson["sections"]))

    def test_teacher_material_is_not_a_public_asset(self) -> None:
        teacher_name = "A_教師版_教學節奏與常見卡點.md"
        self.assertFalse((ROOT / "course" / "content" / teacher_name).exists())
        self.assertFalse(any(path.name == teacher_name for path in self.site.rglob("*")))
        with zipfile.ZipFile(self.site / "downloads" / "ScoreSense_逐步專題講義_v2_學生版.zip") as bundle:
            self.assertFalse(any(teacher_name in name or "/private/" in name for name in bundle.namelist()))

    def test_hackmd_examples_inside_fences_are_preserved(self) -> None:
        source = (ROOT / "course" / "content" / "C_HackMD排版與貼上說明.md").read_text(encoding="utf-8")
        normalized = build_course.normalize_hackmd(source)
        self.assertNotIn("\n[TOC]\n\n---", normalized)
        self.assertIn("```markdown\n[TOC]\n```", normalized)
        self.assertIn("```markdown\n:::info\n這是補充資訊。\n:::\n```", normalized)
        lesson = next(item for item in self.lessons if item["id"] == "C")
        self.assertIn("[TOC]", lesson["html"])
        self.assertIn(":::info", lesson["html"])

    def test_archives_are_public_and_reproducible(self) -> None:
        archives = sorted((self.site / "downloads").glob("*.zip"))
        before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in archives}
        for archive in archives:
            with zipfile.ZipFile(archive) as bundle:
                self.assertTrue(bundle.namelist())
                self.assertTrue(all(entry.date_time == (1980, 1, 1, 0, 0, 0) for entry in bundle.infolist()))
        build_course.main()
        after = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in archives}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
