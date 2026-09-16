import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

from app.services.musicxml import annotate_musicxml


SAMPLE = """<?xml version='1.0' encoding='UTF-8'?>
<score-partwise version='4.0'>
  <part-list><score-part id='P1'><part-name>Music</part-name></score-part></part-list>
  <part id='P1'><measure number='1'>
    <note><pitch><step>C</step><octave>4</octave></pitch><duration>1</duration></note>
    <note><pitch><step>F</step><alter>1</alter><octave>4</octave></pitch><duration>1</duration></note>
    <note><rest/><duration>1</duration></note>
  </measure></part>
</score-partwise>
"""


class MusicXMLTests(unittest.TestCase):
    def test_annotation(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "in.musicxml"
            dst = Path(td) / "out.musicxml"
            src.write_text(SAMPLE, encoding="utf-8")
            notes = annotate_musicxml(src, dst, "solfege")
            self.assertEqual([n.label for n in notes], ["Do", "Fa♯"])
            root = ET.parse(dst).getroot()
            texts = [el.text for el in root.iter() if el.tag.endswith("text")]
            self.assertIn("Do", texts)
            self.assertIn("Fa♯", texts)


if __name__ == "__main__":
    unittest.main()
