# ScoreSense 協作契約

## 目的與範圍

這是自主學習用樂譜辨識與自動標註本機原型。沿用 Python、OpenCV、選配 oemer、ElementTree、FastAPI 與靜態 OSMD 網頁；沒有 music21 或 Flutter。成熟度 prototype；上傳與持久檔案風險 R3，不因展示用途而視為已具公開服務安全性。

當前功能是前處理、圖片轉 MusicXML、固定 Do 三模式與 MusicXML 標註。首調、完整簡譜、PDF／圖片匯出、多頁、App 與雲端為後續工作，不能由初始化或文件任務推定授權。課程內容是需求來源，不是已通過的功能／學習成果。

## 元件、責任與事實來源

只有一個邏輯元件 `core`，runtime 與 requirements 在根目錄。保持既有結構，`app/` 是 Python package；不為命名規範搬移。

| 責任 | 路徑 |
| --- | --- |
| 命令／設定／環境 | main.py、doctor.py、app/config.py、requirements*.txt、run_* |
| 前處理／模型介接 | app/services/image_preprocessor.py、omr.py、scripts/download_omr_models.py |
| 音高／標註 | app/services/converter.py、musicxml.py |
| 流程與 API | app/services/pipeline.py、app/web.py |
| 網頁與設計實作來源 | static/ |
| 驗證 | tests/、samples/；data/ 是使用者或產生資料，非測試真值來源 |

文件權責：`docs/project-profile.md` 管定位與未決事項；`docs/requirements.md` 管需求及課程對照；`docs/project-capabilities.md` 管能力狀態與責任；`docs/architecture.md` 管架構、API、資料、儲存、安全、整合與部署邊界；`docs/local-development.md` 管環境與命令；`docs/acceptance.md` 管證據；README 是入口，AGENTS 是工作契約。修改事實時同一任務同步權責文件，避免複製另一套規格。

## 工作方式與能力狀態

先讀相關規則、程式、文件、環境與現有變更，再界定需求。將事實區分已確認、規劃、已實作、已驗證、模擬、不可用、延後與未決。

能力狀態僅用 `required`、`optional_later`、`not_needed`、`unresolved`；required 是當前責任，不代表已通過。未決事項停止其受影響工作，延後項目不授權新增程式或外部資源。

流程：分類 → 對照能力、owner、文件與驗證 → 完成已授權修改 → 相關驗證 → 同步文件 → 檢查實際差異並回報。不要增加不必要的框架、流程文件或通用重構。只有實質影響方向、安全或授權的資訊缺口才詢問。

## 多 Agent

主代理依收益決定分工，明確給出目的、可寫路徑／能力、介面、測試、文件與授權邊界。預設少量完整任務；不得平行改寫同一檔案。子代理先檢查原始證據，保護既有改動，不跨 owner 或自行再委派；衝突回報主代理。

每個代理回報實際修改路徑、命令、結果、文件、假設與風險；不得將其他代理測試當成自己執行。主代理檢查合併後真實差異與整合證據，不能只接受成功宣稱。

Superpowers 預設停用，僅使用者當前訊息以明確 plugin tag 啟用才使用；任務類型不構成啟用。

## 資料、安全與批准邊界

- 保留既有程式、環境、模型、原始樂譜與工作產物，不擅自清除 data 或重裝依賴。
- 維持本機 127.0.0.1。無登入、檔案擁有者驗證、上傳／解壓容量限制與佇列；job ID 不是授權。公開服務需另案安全設計及批准。
- 只處理有權使用的樂譜，輸入可能含個人註記與版權內容；不把真實上傳、日誌、機密或模型快取納入提交。
- 儲存、保存期限、刪除、備份與遷移由使用者決定；備份／還原未驗證。原檔與衍生檔分開，不能批次轉換或覆寫原稿。
- 設計權威是 static 現有程式。參考圖不代表全面改版授權，不捏造設計檔。
- 新服務、外部傳訊、帳號／權限變更、付費、授權選擇、公開內容、部署及破壞性操作需明確授權。一般範圍內可逆本機文件與驗證直接做。
- 不自行初始化 Git、建立 branch／remote、commit、PR、merge、push、release 或部署；各操作授權不互相涵蓋。

## 開發與品質

現有 Python 3.11.14 已驗證：

```bash
.venv/bin/python doctor.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python main.py process samples/twinkle.musicxml --mode zhuyin
```

測試 7/7 通過，CLI 範例 7 音符，詳見 acceptance。Web 指令 `.venv/bin/python main.py web` 預設 port 8000；本次 bind 被環境禁止，未確認 HTTP 或視覺驗收。真實圖片 OMR、新環境安裝與跨平台未驗證。沒有既定 lint／typecheck／build／CI 命令。

`OEMER_COMMAND` 是選配完整執行檔路徑；不含 shell 參數，程式不讀 .env。不得寫入真實秘密或由私人設定抄出範例。健康檢查僅找命令，不保證推論正常；網頁 OSMD 依賴 CDN。

## Git 與交付

目前不是 Git repository；以下規則在操作具備前提及明確授權後適用。無 Git 時以修改前備份／內容比對檢查差異，不捏造 branch 或 remote。

# 個人專案 Git、Commit 與分支規範

建立或更新個人專案的 `AGENTS.md` 時，完整寫入本規範；後續每一次 branch、commit、merge、push 或 PR 都適用。先判斷使用者這次明確授權與 repository 狀態，不得把 commit 授權擴大為 merge、push、release 或 deployment 授權。

## 操作前檢查

每次 Git 操作前執行：

```bash
git status --short --branch
git branch --show-current
git remote -v
```

確認 working tree 是否乾淨、變更是否屬於同一任務、所在 branch、remote 是否存在，以及使用者明確授權的操作。沒有 remote 時，只進行已授權的本機操作；不得虛構 push、PR 或遠端 URL。

## Branch

正式修改預設從最新 `main` 建立短期 branch：

```text
<type>/<short-topic>
```

允許的 type 為 `feature`、`fix`、`docs`、`chore`、`refactor`、`test`、`build`、`ci`、`release`、`hotfix`。`short-topic` 使用小寫英文 kebab-case，不得包含個資、憑證、私密筆記或未公開資料。

同一任務進行中或只建立 checkpoint commit 時維持目前 branch。下一個獨立任務從最新 `main` 另開 branch；不得為了整潔刪除仍有未完成工作、獨有 commit 或衝突的 branch。

## Commit Format

使用 Conventional Commits：

```text
<type>(<scope>): <簡短繁體中文描述>
```

- `type` 和 `scope` 是機器可讀識別，維持英文；subject 和 body 預設使用繁體中文。
- `scope` 可省略。優先使用實際 component 或責任範圍，例如 `web`、`app`、`backend`、`worker`、`cms`、`docs`、`deps`、`infra` 或 `repo`；不要發明不對應任何檔案或責任的 scope。
- 常用 `type`：`feat`、`fix`、`docs`、`chore`、`refactor`、`test`、`build`、`ci`、`style`、`perf`、`revert`。
- 每筆 commit 只表達一個可獨立理解與回滾的目的。subject 要具體描述成果；不要使用「更新」、「修正問題」、「WIP」、「測試」或「最終版」等模糊文字。
- 在 body 記錄必要的原因、風險、驗證結果、migration、環境影響或 breaking change；沒有這些資訊時，不要為了格式寫空 body。

範例：

```text
feat(web): 新增每日摘要卡片
fix(backend): 修正匯入資料的日期解析
docs: 補充本機啟動與驗證步驟
chore(init): 初始化個人專案結構
```

## Commit、Merge 與 Push 授權

- 使用者只要求 `commit` 時，只提交已驗證、同一任務且可理解的變更，並維持在目前 branch；不得 merge、刪 branch、push、建立 PR、release 或 deployment。
- 使用者要求合併進 `main` 時，完成必要的同任務 commit 與品質檢查，安全合併並驗證 `main`。只有確認 branch 已完整合併、沒有獨有 commit 且沒有待續工作後，才使用 `git branch -d <branch>`；不得使用 `git branch -D`。
- 使用者要求 push 時，只推送已存在且通過檢查的 commit。即使 remote 存在，也不得推定已獲得 push 授權。
- 已設定 GitHub remote 且使用者同時授權 merge 與 push 時，遵守現有 branch protection；有既定 PR 流程時，推送任務 branch 並走 PR，而非繞過保護直接推送 `main`。

## Commit 前安全與品質檢查

每次使用者要求 commit、merge 或 push 前：

1. 檢查 staged、unstaged、untracked 檔案與 diff。
2. 檢查 API key、token、password、private key、cookie、credential、真實 `.env`、個資、私密資料集、未公開筆記、合約或其他不應公開的檔案。
3. 將不應提交的檔案移出 staging，更新 `.gitignore`，並改用 `.env.example` 或安全 placeholder；若憑證可能已暴露，停止並提醒輪替。
4. 只 stage 明確路徑；不得使用 `git add .`。
5. 執行適用且已驗證的品質檢查，並同步 README、AGENTS、元件 README 與受影響的 `docs/`。

資料分類或提交範圍無法安全判斷時，停止並詢問使用者。

## 完成回報

回報改動與保留範圍、實際命令與結果、文件同步、未驗證項目、風險與 Git／遠端狀態。採用其他代理證據時標明來源並確認受測狀態；未跑視覺、整合或部署檢查要說明原因。無文件變更時說明為何權責文件仍符合實作。合約、報價、個資及其他敏感文件預設不得提交；操作後再檢查剩餘變更，不夾帶無關內容。
