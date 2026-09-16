import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from app.services.omr import find_oemer


class OMRCommandTests(unittest.TestCase):
    def test_finds_environment_command_without_activated_path(self):
        with tempfile.TemporaryDirectory() as directory:
            command = Path(directory) / 'oemer'
            command.touch()
            with patch.dict('os.environ', {}, clear=True), patch('sys.executable', str(Path(directory) / 'python')), patch('shutil.which', return_value=None):
                self.assertEqual(find_oemer(), str(command))

    def test_explicit_command_takes_priority(self):
        with patch.dict('os.environ', {'OEMER_COMMAND': '/custom/oemer'}):
            self.assertEqual(find_oemer(), '/custom/oemer')
