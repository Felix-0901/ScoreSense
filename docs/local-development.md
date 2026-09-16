# 本機開發

## Python 3.11 與平台套件清單

完整的新手步驟見 [第 1 章單元三](../course/content/01_環境安裝與第一支Python程式.md)：先安裝本機 Python，再進入專案根目錄建立 `.venv`，再安裝平台套件；模型準備留待辨識章節。不要在全域 Python 安裝專案依賴。

Windows PowerShell：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8 = "1"
python -m pip install --upgrade pip
python -m pip install -r requirements-omr.txt
```

每次新開終端機，重新啟用環境並設定 UTF-8；不必重裝套件。

macOS（已安裝 Python 3.11）：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-omr-mac.txt
python -m pip install --no-deps oemer==0.1.8
```

若 Homebrew 的 Python 不在 PATH，以 `"$(brew --prefix python@3.11)/bin/python3.11"` 建立環境。

| 清單 | 用途 |
| --- | --- |
| requirements.txt | 核心 API 與 OpenCV，NumPy 1.26.4 |
| requirements-omr-common.txt | 引入核心清單，固定共同 OMR 依賴並包含 requests |
| requirements-omr.txt | Windows oemer 0.1.8、ONNX Runtime GPU 1.17.1 |
| requirements-omr-mac.txt | 引入共同清單，使用 ONNX Runtime CPU 1.18.1 |
| requirements-course.txt | 獨立教材建置依賴，非辨識 runtime 必需 |

直接依賴已固定主要相容版本，但沒有完整傳遞依賴鎖檔。

Mac 用 CPU runtime 替代 oemer 宣告的 GPU runtime，因此 `pip check` 仍可能回報 oemer 缺少 onnxruntime-gpu。這是上游 metadata 限制，並非可藉升降 NumPy 消除的衝突；不能在 Mac 安裝 CUDA 套件，也不要混裝兩個 runtime。其他依賴錯誤仍須處理。

## 模型、啟動與驗證

環境啟用後兩平台使用相同命令：

```bash
python scripts/download_omr_models.py
python doctor.py
python -m pip check
python main.py process samples/twinkle.musicxml --mode zhuyin
python main.py web --host 127.0.0.1 --port 8000
```

模型腳本使用 GitHub，沿用 `data/models/` 快取，並複製至目前虛擬環境的 oemer checkpoints。兩個模型都必須載入成功。網頁入口為 `http://127.0.0.1:8000/`，按 Ctrl+C 停止。

`doctor.py` 和 `/api/health` 只檢查命令存在，不代表模型推論已通過。教材第 1 章僅準備環境，模型與真實圖片驗證留待後續辨識章節。

Windows 安裝清單通過依賴檢查；macOS ARM64／x86_64 通過套件解析與 wheel 可用性檢查，尚未在 Mac 實機驗證。

原始 Windows 測試仍有一項 `test_finds_environment_command_without_activated_path` 因測試建立無 .exe 的假命令而失敗；實際 oemer.exe 查找正常。本次未更動應用程式與測試。

## 設定與 CLI

唯一應用程式環境變數是選配 `OEMER_COMMAND`：完整執行檔路徑，不是附帶參數的 shell 字串。未設定時依 Python 環境旁的 oemer，再查 PATH。程式不自動讀 `.env`，因此未建立 `.env.example`；需要覆寫時在啟動程序的 shell 設定。

`process` 支援 `--mode solfege|numbered|zhuyin`、`--output`、`--no-preprocess`、`--hide-accidental`、`--show-octave`。`preprocess <圖片路徑>` 可單獨產生前處理，預設寫至 `data/preprocess_demo/`。這些其餘選項本次未逐項執行。

目前沒有專案 lint、typecheck、build 或 CI 命令；不要虛構通過。一般修改依風險執行 unittest、CLI、API／瀏覽器或 OMR 驗證；文件修改核對路徑、程式事實與差異即可。

## 靜態教室建置

使用獨立 Python 環境安裝 `requirements-course.txt`，執行 `python scripts/build_course.py`，再以 `python3 -m http.server 18766 --bind 127.0.0.1 --directory course/site` 預覽。完整命令與 Pages 自動部署與手動重跑步驟見 [course/README.md](../course/README.md)。教材網站不依賴既有 `.venv`、oemer 或 OSMD CDN。
