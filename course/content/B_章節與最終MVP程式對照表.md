# 章節與最終 MVP 程式對照表

這份表格給教師與後期複習使用。

| 教材章節 | 最終專案主要對應 |
| --- | --- |
| 01～03 | `requirements.txt`、環境與一般 Python 基礎 |
| 04～08 | `app/services/image_preprocessor.py` |
| 09～10 | `app/services/converter.py` |
| 11～14 | `app/services/musicxml.py` |
| 15 | converter + musicxml 的第一個完整子系統 |
| 16～17 | `requirements-omr.txt`、`app/services/omr.py` |
| 18 | image_preprocessor + omr + musicxml 的串接 |
| 19 | `app/` package 與正式資料夾 |
| 20 | `app/services/pipeline.py`、`app/config.py` |
| 21 | `main.py` |
| 22 | `tests/`、`doctor.py` |
| 23 | `app/web.py` |
| 24 | `static/index.html`、`static/app.js`、`static/styles.css` |
| 25 | 全專案 |
| 26 | 成果測試與後續擴充 |

---

## 為什麼教材程式不一開始就和 MVP 完全一樣？

因為正式程式碼通常包含：

```text
相容性
錯誤處理
多格式
封裝
路徑管理
型別
重試
API
安全檢查
```

如果第一天全部出現，初學者只會看到一大片陌生語法。

教材會先寫「最小可理解版本」，確認觀念後再逐步演化到正式版本。

這不是簡化到錯誤，而是**控制一次出現的新概念數量**。
