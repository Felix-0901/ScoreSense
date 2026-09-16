# ScoreSense｜樂譜辨識與自動標註系統

將樂譜圖片或 MusicXML 轉成附有 Do Re Mi、數字或注音唱名的樂譜，作為自主學習專題與教學實作。

> 狀態：本機原型（prototype）。MusicXML 標註範例與 7 項單元測試已通過；圖片 OMR、瀏覽器排版與跨平台安裝尚未完成本次端到端驗證。不是已部署的公開服務。

## 目前功能

- 圖片灰階、對比增強、傾斜估計與校正，以及二值化教學預覽。
- 透過選配 oemer 將圖片轉成 MusicXML；可直接輸入 `.xml`、`.musicxml`、`.mxl` 跳過 OMR。
- 固定 Do 的 `solfege`、`numbered`、`zhuyin` 三模式，支援升降記號與簡單八度箭頭。
- 將標註寫入 MusicXML 第 99 號歌詞行，保留其他歌詞行；原有第 99 號行會被替換。
- CLI、FastAPI API 與網頁上傳介面，輸出 MusicXML、音符 JSON，透過 OpenSheetMusicDisplay 顯示。

數字模式是固定音名對應 1–7，尚非完整簡譜排版或首調唱名。目前使用 Python 標準函式庫解析 MusicXML，**沒有使用 music21**。Flutter App、PDF／圖片匯出、多頁處理與辨識準確率評測仍屬後續範圍。

## 本機開始

現有環境已確認為 Python 3.11.14。在專案根目錄使用既有虛擬環境：

```bash
.venv/bin/python doctor.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python main.py process samples/twinkle.musicxml --mode zhuyin
```

最後一項已實測產生 7 個標註音符，結果在 `data/outputs/<job_id>/`。

本機網頁入口：

```bash
.venv/bin/python main.py web
```

預設網址為 `http://127.0.0.1:8000`。本次執行環境禁止監聽本機連接埠，因此未驗證 HTTP／瀏覽器流程。新環境安裝、OMR 安裝與 CLI 選項見[本機開發](docs/local-development.md)。OSMD 由 CDN 載入，樂譜顯示需要網路。

## 專案結構

```text
main.py                  CLI 與本機 Web 入口
app/config.py            本機資料路徑與支援副檔名
app/web.py               FastAPI 路由
app/services/            前處理、OMR、MusicXML、音名轉換與流程整合
static/                  HTML、CSS、JavaScript 介面
samples/                 示範 MusicXML
scripts/                 OMR 模型下載工具
tests/                  unittest 測試
data/                   本機上傳、工作檔、輸出與模型（不提交）
```

保留既有單一 Python 專案結構；前端由同一服務提供，不另建前端框架或獨立後端目錄。

## 文件與協作

- [AGENTS.md](AGENTS.md)：人員與 Agent 的維護契約、驗證與 Git 授權。
- [專案定位](docs/project-profile.md)：成熟度、範圍、風險與未決事項。
- [需求與課程對照](docs/requirements.md)：三階段與十章的實作邊界。
- [架構與資料邊界](docs/architecture.md)：API、儲存、安全、第三方整合。
- [能力與維護責任](docs/project-capabilities.md)：十類能力與驗證責任。
- [本機開發](docs/local-development.md)、[驗收證據](docs/acceptance.md)。

目前沒有 Git repository／remote，未初始化、提交或發布。專案授權尚未選定；[THIRD_PARTY.md](THIRD_PARTY.md) 是既有第三方元件清單，公開發布前仍需確認套件、模型與示範樂譜的授權。
