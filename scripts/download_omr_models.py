"""Install the two official ONNX checkpoints used by oemer (no TensorFlow weights)."""
from importlib.util import find_spec
from pathlib import Path
import shutil
import requests
import onnxruntime

root = Path(__file__).resolve().parents[1]
spec = find_spec('oemer')
if spec is None or spec.origin is None:
    raise SystemExit('Install oemer first; see README.md.')
package = Path(spec.origin).parent
for name, folder in [('1st_model.onnx', 'unet_big'), ('2nd_model.onnx', 'seg_net')]:
    destination = package / 'checkpoints' / folder / 'model.onnx'
    if destination.exists():
        onnxruntime.InferenceSession(str(destination), providers=['CPUExecutionProvider'])
        print('Ready:', destination)
        continue
    cached = root / 'data' / 'models' / (name + '.complete')
    cached.parent.mkdir(parents=True, exist_ok=True)
    if not cached.exists():
        partial = cached.with_suffix('.part')
        url = 'https://github.com/BreezeWhite/oemer/releases/download/checkpoints/' + name
        with requests.get(url, stream=True, timeout=(30, 120)) as response:
            response.raise_for_status()
            with partial.open('wb') as output:
                for chunk in response.iter_content(1024 * 1024):
                    output.write(chunk)
        onnxruntime.InferenceSession(str(partial), providers=['CPUExecutionProvider'])
        partial.replace(cached)
    onnxruntime.InferenceSession(str(cached), providers=['CPUExecutionProvider'])
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cached, destination)
    print('Ready:', destination)
