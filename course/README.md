# ScoreSense 逐步專題教室

獨立的靜態教材網站；保留原本 Python/FastAPI 樂譜辨識系統。課程 00 為導讀，01–26 為循序實作，B/C/D 與 README 為補充，共 31 篇公開教材。

## 本機建置與預覽

在專案根目錄執行（另用虛擬環境，不改既有 OMR 環境）：

```bash
python3 -m venv /tmp/scoresense-course-venv
/tmp/scoresense-course-venv/bin/python -m pip install -r requirements-course.txt
/tmp/scoresense-course-venv/bin/python scripts/build_course.py
python3 -m http.server 18766 --bind 127.0.0.1 --directory course/site
```

開啟 http://127.0.0.1:18766/ 。網站以 HTTP 讀取 `lessons.json`，不要直接雙擊 HTML。

- 修改教材：`course/content/*.md`，重新建置。
- 介面：`course/site/index.html`、`styles.css`、`app.js`。
- 建置結果：`lessons.json`、`materials/`、`downloads/`，不提交產物。
- 教師 A：只保留於 `course/private/`，Git 忽略，公開建置不依賴此資料夾。
- 學習進度：瀏覽器 localStorage，沒有登入、跨裝置同步或伺服器資料。
- 下載的參考專案為原教材版本，不會隨本機核心程式更新。

## GitHub Pages

教學網站已上線：[ScoreSense 逐步專題教室](https://felix-0901.github.io/ScoreSense/)。origin 為 https://github.com/Felix-0901/ScoreSense.git ，使用 `main`。

`.github/workflows/course-pages.yml` 在每次 push 到 `main` 時自動建置並部署，亦保留 `workflow_dispatch` 手動重跑。GitHub Pages 的 Source 使用 **GitHub Actions**。

日後更新流程：

1. 修改 `course/content/*.md` 教材或 `course/site/` 介面，依本文件建置並預覽。
2. 檢查變更後 commit，執行 `git push origin main`。
3. 到 Actions → **Deploy ScoreSense classroom**，確認該次 commit 的 `build` 與 `deploy` 都成功。
4. 重新整理教學網站，核對更新內容。部署完成前仍會顯示前一版；若失敗，查看失敗步驟的日誌，修正後再推送。

需要手動重跑時，在上述 workflow 點 **Run workflow**，選 `main`。不需另提交編譯後的 JSON、素材副本或 ZIP。

Workflow 安裝教材編譯器，產生並僅上傳 `course/site/`；不發布 Python API、模型、data 或教師資料。採相對資源 URL 與 hash 導覽，同時支援使用者根站與 `/repository/` 專案網址，無需自訂網域或後端。

參考：[GitHub 官方 Pages 自訂 workflow 文件](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 教材使用

先從第 01 章學起，完成第 25 章後再核對完整 MVP；原教材中的安裝命令與範例完整保留，未宣稱所有平台／課堂範例均經實際執行。網站提供程式碼複製、全文搜尋、章內目錄、列印及完成標記；Python／OMR 實驗仍在學生自己的電腦執行。
