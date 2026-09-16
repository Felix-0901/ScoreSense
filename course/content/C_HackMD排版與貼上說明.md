# HackMD 排版與教材貼上說明

這份教材以 HackMD 可直接使用的 Markdown 為主。

[TOC]

---

## 一、標題

```markdown
# 第 1 章
## 單元一
### 小節
```

HackMD 會把第一個一級標題當成主要標題。

---

## 二、目錄

教材使用：

```markdown
[TOC]
```

貼到 HackMD 後會依標題自動產生目錄。

---

## 三、程式碼

```markdown
```python
print("hello")
```
```

HackMD 支援語法高亮。

如果需要行號，也可以在 HackMD 使用帶行號的 code block 語法；本教材預設不用，避免複製到其他平台時不相容。

---

## 四、提示框

HackMD 支援：

```markdown
:::info
這是補充資訊。
:::
```

以及：

```markdown
:::warning
這是注意事項。
:::
```

教材只在真的需要強調時使用，不會每段都塞提示框。

---

## 五、表格與勾選

```markdown
| 項目 | 結果 |
| --- | --- |
| 測試 | OK |
```

```markdown
- [ ] 尚未完成
- [x] 已完成
```

很適合里程碑驗收。

---

## 六、建議的 HackMD 管理方式

每一個 Markdown 檔建立一篇 Note。

命名可直接沿用：

```text
01｜環境安裝與第一支 Python 程式
02｜Python 資料結構、函式與模組
...
```

另外把 `00_課程總目錄與學習地圖.md` 當課程首頁。

如果 HackMD URL 已經建立，可以再把每章連結補回總目錄，變成真正可點擊的課程入口。
