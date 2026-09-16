# 架構、資料與整合

## 執行與資料流

```text
CLI main.py / 瀏覽器 static → FastAPI app/web.py
                         → process_file
圖片 → OpenCV 前處理（可關閉）→ oemer subprocess → MusicXML
MusicXML / MXL ────────────────────────────────┘
 → ElementTree 解析 → pitch_to_label → lyric 99 → MusicXML + notes.json
 → 瀏覽器 OpenSheetMusicDisplay（jsDelivr CDN）
```

`app/services/pipeline.py` 整合流程；`converter.py` 負責固定 Do；`musicxml.py` 處理 XML/MXL、跳過休止符與無 pitch 的音符、逐音標註並記錄和弦音旗標。沒有完整節奏分析、首調推算或和弦排版策略，也沒有 music21 依賴。

前處理輸出 `preprocessed.png` 給 OMR；`binary_preview.png` 用於觀察二值化，不是 OMR 實際輸入。沒有透視校正或自動背景裁切的保證。

OMR 先執行一般命令，失敗再加 `-d` 停用 oemer 自身 deskew；每次 timeout 1800 秒，最多兩次，故整體可能接近 3600 秒。API 在 async handler 直接跑同步流程，無工作佇列、取消或真實進度回報。

## API 契約

| 路由 | 作用 |
| --- | --- |
| `GET /`、`/static/*` | 網頁與靜態資源 |
| `GET /api/health` | `ok`、`oemer_available`、`supported_modes`；只判斷命令可找到，不證明模型可推論 |
| `POST /api/process` | multipart：`file`、`mode=solfege`、`preprocess=true`、`show_accidental=true`、`show_octave=false` |
| `GET /api/files/{job_id}/{filename}` | 下載輸出檔 |
| `GET /api/work/{job_id}/{filename}` | 讀取工作產物與 OMR 日誌 |

成功回傳 job ID、音符數、前 24 音符預覽、MusicXML／JSON URL，以及有產生時的前處理、二值化與日誌 URL。模式錯誤／ValueError 為 400，OMR 不可用為 503，OMR 失敗為 422，其餘例外為 500；框架欄位驗證亦可能回 422。

## 儲存與安全邊界

provider／local_model：filesystem。owner_component：core。access_profile：本機無驗證 HTTP 檔案路由，**不是 private_proxy 或授權私有儲存**。

| 路徑 | 用途與保留 |
| --- | --- |
| `data/uploads/<job_id>/` | API 保存原始上傳；CLI 讀取原輸入 |
| `data/work/<job_id>/` | MusicXML 副本、前處理、OMR 檔案與日誌 |
| `data/outputs/<job_id>/` | 標註 MusicXML 與 notes.json |
| `data/models/` | 模型下載快取；腳本也複製至虛擬環境內 oemer checkpoints |

job ID 為 UUID hex 前 12 字元，不是存取權杖。檔案會留在磁碟，重啟不自動清除；無保存期限、磁碟配額、自動備份或還原驗證。使用者負責決定作品備份；不得擅自清空既有 `data/`。遷移時先確認要保留的原始與輸出資料、複製並比對後才考慮切換，未實作遷移工具。

目前沒有登入、擁有者驗證、上傳大小限制、MXL 解壓資源上限、工作隔離與完整不可信輸入防護。檔案路徑有檢查，但未完成安全測試，不能當成公開服務的安全保證。維持 `127.0.0.1`；公開存取前必須另行設計與驗收上述限制。僅用有權處理的檔案，日誌可能含本機路徑，不任意公開。

保留使用者原檔；前處理只寫衍生檔。不將樂譜、MusicXML、截圖或文件當成展示照片批次轉 WebP。

## 第三方與交付

Python 套件由 requirements 檔管理，未有完整傳遞依賴鎖檔。oemer 為選配本機推論；模型下載來源由 `scripts/download_omr_models.py` 指向 GitHub，並非自行訓練。瀏覽器從 jsDelivr 取得 OSMD 1.9.7；這是網路依賴，未實作離線封裝。沒有已設定的付費 API、資料庫、容器或雲端。

`THIRD_PARTY.md` 是元件清單而非完整授權稽核。公開、再散布或更換模型前需核對實際授權；這次沒有選定專案 LICENSE，也沒有發布／備份／回滾的生產證據。

## 靜態教室（2026-09-16）

`course/content/` Markdown → `scripts/build_course.py` → `course/site/lessons.json` 與素材／ZIP。`course/site/index.html`、CSS、JavaScript 提供 hash 章節導覽、全文搜尋、章節進度與列印；不呼叫 FastAPI。瀏覽器僅以 localStorage 保存完成章節及最後閱讀章節，無同步或帳號。所有網站資源使用相對 URL，支援 GitHub Pages repository 子路徑。

教師 A 原文放 `course/private/` 並 Git 忽略，不進入公開產物。公開來源 ZIP 包含其他教材與來源參考程式，參考程式是教材快照。Pages workflow 每次 push 到 `main` 自動執行，亦保留手動觸發，artifact 限 `course/site/`；本機上傳、模型與工作產物不在 artifact。原本 core 的本機安全邊界維持不變。
