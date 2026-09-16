# 能力與維護責任

狀態描述範圍，不代表完成度。`required` 當前必需、`optional_later` 延後不授權實作、`not_needed` 本階段無需、`unresolved` 需決策且阻擋受影響操作。

十類 coverage：product、architecture、design、data、security、integration、quality、delivery、operations、documentation 均為 `required`（僅既有本機原型範圍）。資料庫、登入服務與雲端部署為 `not_needed`；未來公開服務必須重新評估。

每列 owner_components 均為 `core`（唯一執行元件），下列路徑標示內部責任；指定到實際人員／Agent 時由主代理分配。每列維護規則為任務負責人修改時同步權責文件、主代理核對差異與證據。approval 是變更該項重要決策所需批准，不是每次唯讀檢查的關卡。

| id／能力 | category | status | 責任路徑 | documents | verification | decisions／maintenance | approval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `label` 固定 Do 三模式 | product | required | converter.py／musicxml.py | [requirements.md](requirements.md) | 既有 converter 與 MusicXML 測試；CLI 範例 | 保留第 99 行替換語義 | none |
| `flow` 單 runtime 與流程 | architecture | required | pipeline.py／web.py | [architecture.md](architecture.md) | CLI 通過；HTTP 未驗證 | 維持原結構與 API 契約 | none |
| `ui` 上傳與樂譜顯示 | design | required | static/ | [requirements.md](requirements.md) | 瀏覽器與注音排版待驗證 | 以既有 static 為設計來源 | none |
| `files` 本機檔案保存 | data | required | config.py／pipeline.py | [architecture.md](architecture.md) | 核對資料目錄；CLI 已產物 | 不自動清除，保留期限未決 | user |
| `local-boundary` 上傳與本機存取 | security | required | web.py | [architecture.md](architecture.md) | 程式唯讀核對；安全測試未完成 | 維持 loopback，不宣稱私有授權 | user |
| `omr` 圖片辨識與模型 | integration | required | omr.py／download_omr_models.py | [architecture.md](architecture.md) | 命令查找測試；真實推論待驗證 | 失敗重試與模型依賴分別核對 | none |
| `render` OSMD CDN | integration | required | static/index.html | [architecture.md](architecture.md) | CDN／排版未驗證 | 固定現有版本；離線未支援 | none |
| `checks` 核心回歸與驗收 | quality | required | tests/ | [acceptance.md](acceptance.md) | 7 項 unittest 通過 | 修改受影響邊界後更新證據 | none |
| `run` 本機 CLI／Web 交付 | delivery | required | main.py／run_* | [local-development.md](local-development.md) | CLI 通過；Web bind 受限 | 新環境與平台各自驗證 | none |
| `diagnostics` 環境與保留管理 | operations | required | doctor.py／data/ | [architecture.md](architecture.md) | imports 可用；備份還原未驗證 | doctor 不等於健康推論；刪除先授權 | user |
| `docs` 課程與實作同步 | documentation | required | README.md／AGENTS.md／docs/ | [project-profile.md](project-profile.md) | 文件連結與原始碼核對 | 隨功能與驗收同任務同步 | none |
| `extensions` 首調／PDF／App | product | optional_later | 無實作 owner 路徑 | [requirements.md](requirements.md) | 尚未實作與驗收 | 需求另案確認後指定 owner | user |
| `release-license` 公開再散布授權 | delivery | unresolved | THIRD_PARTY.md | [project-profile.md](project-profile.md) | 未選專案 LICENSE，未完整授權盤點 | 公開前確認程式、模型與樂譜權利 | user |

## 靜態教材交付責任

`classroom`：required；owner_components：core；責任路徑 `course/`、`scripts/build_course.py`、`requirements-course.txt`、`.github/workflows/course-pages.yml`；權責文件為 `course/README.md`、architecture、requirements、acceptance。維護時重建教材並驗證章節與資源隔離、桌機／手機閱讀；使用者已授權 main push 自動部署教室，保留手動重跑。原先雲端 not_needed 指辨識 runtime；靜態教材已於 https://felix-0901.github.io/ScoreSense/ 上線。
