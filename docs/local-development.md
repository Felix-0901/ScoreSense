# 本機開發

## 現有環境與已驗證命令

在根目錄執行。2026-09-16 已確認 macOS arm64、Python 3.11.14、OpenCV 4.8.1、FastAPI 0.128.2、Uvicorn 0.48.0、multipart 0.0.20。

```bash
.venv/bin/python doctor.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python main.py process samples/twinkle.musicxml --mode zhuyin
```

本次 7 個測試通過；範例輸出 7 個音符。doctor 只檢查部分 imports 與 oemer 命令位置，退出成功不代表 OMR 模型已驗證。

## 網頁啟動（程式存在，HTTP 本次未驗證）

```bash
.venv/bin/python main.py web
```

預設 `127.0.0.1:8000`，可用 `--port` 調整。本次於 18764 測試時遭執行環境拒絕 bind：`operation not permitted`。可在一般本機終端啟動後讀取 `/api/health`，上傳 `samples/twinkle.musicxml` 核對三種模式、顯示與下載。`run_mac_linux.sh` 使用 `.venv/bin/python`；`run_windows.bat` 使用 PATH 的 `python`，先啟用對應環境。Windows／Linux 未驗證。

## 新環境安裝（沿用原文件，未重新安裝驗證）

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows 啟用方式為 `.venv\Scripts\activate`。不要覆蓋已有虛擬環境或自行升級依賴；requirements 固定直接依賴版本，但不保證完整可重現。

### 選配 OMR

macOS CPU 路徑，沿用既有專案安裝方式（本次未執行安裝與下載）：

```bash
.venv/bin/python -m pip install -r requirements-omr-mac.txt
.venv/bin/python -m pip install --no-deps oemer==0.1.8
.venv/bin/python scripts/download_omr_models.py
.venv/bin/python doctor.py
```

既有文件記載 oemer metadata 要求 `onnxruntime-gpu`，Mac 以 CPU `onnxruntime` 替代，因此 `pip check` 可能仍報缺 GPU 套件；不要因此在 Mac 安裝 GPU 路徑。其他相容 GPU 環境使用 `requirements-omr.txt`，本次未驗證。模型下載會存取 GitHub、寫入本機快取與套件 checkpoints；先確認環境與網路再自行執行。

## 設定與 CLI

唯一應用程式環境變數是選配 `OEMER_COMMAND`：完整執行檔路徑，不是附帶參數的 shell 字串。未設定時依 Python 環境旁的 oemer，再查 PATH。程式不自動讀 `.env`，因此未建立 `.env.example`；需要覆寫時在啟動程序的 shell 設定。

`process` 支援 `--mode solfege|numbered|zhuyin`、`--output`、`--no-preprocess`、`--hide-accidental`、`--show-octave`。`preprocess <圖片路徑>` 可單獨產生前處理，預設寫至 `data/preprocess_demo/`。這些其餘選項本次未逐項執行。

目前沒有專案 lint、typecheck、build 或 CI 命令；不要虛構通過。一般修改依風險執行 unittest、CLI、API／瀏覽器或 OMR 驗證；文件修改核對路徑、程式事實與差異即可。

## 靜態教室建置

使用獨立 Python 環境安裝 `requirements-course.txt`，執行 `python scripts/build_course.py`，再以 `python3 -m http.server 18766 --bind 127.0.0.1 --directory course/site` 預覽。完整命令與 Pages 手動發布步驟見 [course/README.md](../course/README.md)。教材網站不依賴既有 `.venv`、oemer 或 OSMD CDN。
