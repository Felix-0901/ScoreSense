from __future__ import annotations

import importlib
import platform
import shutil
import sys
from app.services.omr import find_oemer


def check_module(name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(name)
        version = getattr(module, "__version__", "installed")
        return True, str(version)
    except Exception as exc:
        return False, str(exc)


print("=== Score Annotator environment doctor ===")
print("Python:", sys.version.replace("\n", " "))
print("Platform:", platform.platform())
print()

for module in ["cv2", "fastapi", "uvicorn", "multipart"]:
    ok, info = check_module(module)
    print(f"{module:12} {'OK' if ok else 'MISSING':8} {info}")

print()
oemer = find_oemer()
print("oemer CLI:", oemer or "NOT FOUND (image -> MusicXML will be unavailable)")

major, minor = sys.version_info[:2]
if (major, minor) == (3, 11):
    print("Python 3.11: recommended for this project.")
else:
    print("NOTICE: Core features may work, but Python 3.11 is recommended for oemer compatibility.")
