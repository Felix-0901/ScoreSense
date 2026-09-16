import unittest

from app.services.converter import LabelMode, PitchInfo, pitch_to_label


class ConverterTests(unittest.TestCase):
    def test_solfege(self):
        self.assertEqual(pitch_to_label(PitchInfo("C", 0, 4), LabelMode.SOLFEGE), "Do")
        self.assertEqual(pitch_to_label(PitchInfo("F", 1, 4), LabelMode.SOLFEGE), "Fa♯")

    def test_numbered(self):
        self.assertEqual(pitch_to_label(PitchInfo("D", -1, 4), LabelMode.NUMBERED), "♭2")

    def test_zhuyin(self):
        self.assertEqual(pitch_to_label(PitchInfo("B", 0, 4), LabelMode.ZHUYIN), "ㄒㄧ")

    def test_octave_marker(self):
        self.assertEqual(
            pitch_to_label(PitchInfo("C", 0, 5), LabelMode.SOLFEGE, show_octave=True),
            "Do↑",
        )


if __name__ == "__main__":
    unittest.main()
