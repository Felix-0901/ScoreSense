# 專案定位

本文件是既有專案文件補齊的定位紀錄，參考使用者提供的「樂譜辨識與自動標註系統」自主學習課程說明與現有原始碼；課程願景不等於已實作或已驗收功能。

| 項目 | 定位 |
| --- | --- |
| 名稱／slug | ScoreSense／scoresense |
| 類型 | 單一 Python 本機工具與 Web 介面 |
| 成熟度 | prototype；非 deployable |
| 作業 | audit_takeover：文件補齊，保留既有可執行程式 |
| 風險 | R3：接受並保存使用者上傳檔案；本次文件編輯本身為低風險 |
| 使用者 | 自主學習學生、教學者與本機展示操作者 |
| 成功訊號 | 能用授權樂譜完成辨識、三模式標註與人工核對，並說明各處理階段 |
| 協作 | 使用者主導；可依任務明確分工給 Agent |
| 部署 | none；僅本機啟動入口，未確認公開部署 |
| 元件 | `core`：根目錄 Python runtime、`app/`、`static/` 共用一組 dependencies |
| structure_exception | 延續根目錄 requirements 與 main.py；app 是 Python package，不是手機 App；無必要為初始化搬移 |

## 範圍與界線

當前：影像前處理、oemer 串接、MusicXML 音高抽取、固定 Do 三模式、標註回寫、API／網頁／CLI。細節由 [requirements.md](requirements.md) 管理。

延後：首調、PDF／圖片匯出、多頁、Flutter、準確率基準。排除：自行訓練 OMR、大規模資料蒐集、帳號系統、雲端與付費服務自動建立。

設計來源為 `static/index.html`、`static/styles.css`、`static/app.js`；未提供 Figma 或其他正式設計資產。保留實作，不另建 design system。

資料類別為使用者原始樂譜、衍生影像、MusicXML、音符報告、推論日誌、模型；可能含版權內容或個人註記。儲存為本機 filesystem，由 core 管理，非私有授權代理；無登入、無檔案讀取身分檢查。詳見 [architecture.md](architecture.md)。

## 本次處理與開放決策

已補 README、AGENTS、能力、需求、驗收、開發與架構文件，補安全忽略規則。保留所有程式、依賴、原始樂譜、既有產物與環境。不建立 Git、CI、Docker、App、雲端服務或 LICENSE。

待決：專案程式授權；模型與樂譜再散布權限；有價值作品的保留／備份期限；日後是否公開服務及其權限／資源限制。這些未決事項僅阻擋對應發布、刪除或架構變更，不阻擋本機教學與文件維護。

## 靜態教室增補（2026-09-16）

新增同 repository 的靜態教材交付物 `course/`，使用 v2 講義逐步完成 Python → 影像 → MusicXML → OMR → 專案化 → Web → 實驗報告。既有 Python core 保留；Pages 僅承載教材與練習下載，不承載辨識服務。已有本機 Git，origin 已由使用者指定為 https://github.com/Felix-0901/ScoreSense.git ，使用 main；Pages 實際上線尚未執行。
