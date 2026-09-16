# 驗收與證據

本次是文件補齊；以下為 2026-09-16 的驗證，不代表全部課程或學生學習成果完成。

| 項目 | 方法 | 結果 |
| --- | --- | --- |
| 環境 imports | `.venv/bin/python doctor.py` | cv2、FastAPI、Uvicorn、multipart 可匯入；找到 oemer 命令 |
| 現有單元測試 | `.venv/bin/python -m unittest discover -s tests -v` | 7/7 通過；converter、基本 MusicXML 標註、OMR 命令查找 |
| 真實 CLI 範例 | `.venv/bin/python main.py process samples/twinkle.musicxml --mode zhuyin` | 7 音符；生成 MusicXML 與 notes.json，job `03eb847584fd` |
| HTTP 啟動 | `.venv/bin/python main.py web --port 18764` | 應用啟動後 bind 被環境拒絕，未通過 HTTP 驗證 |
| 圖片 OMR | 本次未執行 | 現有 data 產物不能代替本次準確率或端到端證據 |
| OSMD／注音視覺 | 本次未執行 | 未確認字型、和弦標註、縮放與下載後顯示 |
| 跨平台／新環境安裝 | 本次未執行 | 不能以現有 Mac 環境推論 Windows、Linux 通過 |

## 後續核心驗收

1. 以有權使用的清晰單頁譜跑圖片前處理、真實 oemer、標註與瀏覽器顯示；保存版本、參數、耗時、原始人工標準答案與結果。
2. 三種模式核對 C–B、升降與八度；確認數字是固定 Do。休止符不標註，和弦逐音資料與畫面分開檢查。
3. 確認保留非第 99 號歌詞、重跑不累積標註；MXL、命名空間與異常 XML 需補專項驗證，現有測試不能涵蓋所有情況。
4. API 上傳、錯誤提示、下載與 OSMD CDN 失敗時的提示逐項實測；命令存在不等於模型可用。
5. 圖片品質比較採同一譜的清晰、傾斜、暗光、過曝與背景干擾版本，配對前處理開／關。記錄音高正確數／標準音符數、漏音與多音、失敗案例；不要把課程示意表當成實測改善。

## 既有稽核與待改善

- must_fix：本機文件補齊範圍內未發現阻擋項；公開服務前的安全與資源控制仍未具備。
- should_improve：補真實圖片基準、HTTP／視覺驗收、異常輸入測試、安裝重現與完整授權盤點。
- optional_later：首調、PDF／圖片匯出、多頁、App；新增功能需另有任務範圍。

沒有修改產品行為，因此沒有新增測試來重複既有實作。沒有 commit、push、部署或 Git 初始化。

## 逐步專題教室驗收（2026-09-16）

- `/tmp/scoresense-course-venv/bin/python -m unittest discover -s tests -p test_course_build.py -v`：4/4 通過；31 篇輸出契約、教師資料隔離、HackMD 程式範例保留、ZIP 可重現性。主代理重跑確認。
- `.venv/bin/python -m unittest discover -s tests -v`：既有 7 項通過；教材測試因核心環境未裝 Markdown 明確略過，已在獨立教材環境驗證。
- `node --check course/site/app.js`、`git diff --check`：通過。
- Playwright 實際瀏覽器：首頁與課程桌機／390px 手機畫面已查看；00–26 全章無頁面水平溢出；搜尋、手機目錄與搜尋送出、進度重整保存、程式複製、章內跳轉、三份 ZIP HTTP 200 通過。
- 本機 `/site/#lesson/24` 子路徑載入、重新整理與素材下載通過，支援 Pages repository 路徑；未實際部署 GitHub。
- 本次未改 Python runtime 與原辨識介面；未重跑 OMR。未逐一執行教材所有程式，不代表教材跨平台安裝或所有課程成果已驗收。
- 已同步 README、AGENTS、需求、架構、定位、能力與本機開發文件。初次網站驗收時未提交或發布；後續使用者已授權 main commit 與 push，origin 指定為 https://github.com/Felix-0901/ScoreSense.git 。Pages 實際發布未執行。

## Pages 上線與自動部署（2026-09-16 後續）

使用者已完成 Pages 設定及首次部署。實查 https://felix-0901.github.io/ScoreSense/ 回傳 HTTP 200；GitHub Actions run `35048909512`、commit `7d22ad3` 結果為 success，取代上述初次驗收時的未部署狀態。

依使用者要求，workflow 新增 `push.branches: [main]`，保留 `workflow_dispatch`；README 新增網站入口，教室 README 與架構、開發、定位、能力、協作文件同步自動部署規則。公開範圍仍只有 `course/site/`，辨識 API、模型、使用者資料與教師版不包含在 Pages artifact。此修改的首次自動部署結果以對應 commit 的 Actions 紀錄為準。
