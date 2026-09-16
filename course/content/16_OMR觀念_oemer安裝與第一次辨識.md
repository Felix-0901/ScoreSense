# 第 16 章｜OMR 觀念、oemer 安裝與第一次辨識

前面我們已經可以處理 MusicXML。現在才加入整個專題最像「AI 辨識」的一段：把樂譜圖片轉成 MusicXML。

## 學習目標

- 分辨 OCR 與 OMR。
- 理解我們不從零訓練模型的原因。
- 安裝並確認 oemer CLI。
- 用命令列把圖片轉成 MusicXML。
- 人工檢查 OMR 輸出是否合理。

[TOC]

---

## 單元一｜OCR 與 OMR

OCR：

```text
文字圖片
↓
辨識
↓
文字
```

OMR：

```text
樂譜圖片
↓
辨識
↓
結構化樂譜資料
```

OMR 不只是「看見一顆黑點」，還要理解：

```text
五線譜位置
譜號
音高
節奏
小節
升降記號
其他符號
```

這比一般文字 OCR 更專門。

---

## 單元二｜為什麼不用自己訓練？

如果從零做完整 OMR AI，需要：

```text
大量標註樂譜
模型設計
GPU 訓練
資料清理
評估
模型部署
```

這會讓專題重心變成「訓練 OMR 模型」，而不是「完成樂譜自動標註產品」。

本專題學習的是：**如何整合成熟工具，並在它前後加入自己的功能。**

---

## 單元三｜oemer 在我們系統裡只負責一件事

```text
輸入：圖片
輸出：MusicXML
```

它不負責：

```text
Do Re Mi
簡譜
注音
網頁介面
系統流程
```

這些仍是我們自己做的。

---

## 單元四｜安裝獨立的 OMR 依賴

本教材建議先完成核心環境，再額外安裝：

`requirements-omr.txt`

```text
oemer==0.1.8
```

執行：

Windows：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-omr.txt
```

macOS / Linux：

```bash
./.venv/bin/python -m pip install -r requirements-omr.txt
```

確認：

```bash
oemer --help
```

或：

```bash
which oemer
```

Windows 可用：

```powershell
where oemer
```

:::warning
OMR 套件牽涉模型與較舊相依套件，是整份課程最容易受電腦環境影響的部分。若某台電腦安裝失敗，不代表前面 15 章白做；可以先用教師提供的 MusicXML 繼續後續功能，再另外解決 OMR 環境。
:::

---

## 單元五｜第一次從命令列辨識

準備一張清楚、正面的樂譜圖。

在新的空資料夾中執行：

```bash
oemer path/to/score.png
```

完成後找：

```text
.musicxml
.xml
.mxl
```

實際檔名依工具輸出而定。

---

## 單元六｜不要只看「成功」兩個字

打開產生的 MusicXML，檢查：

1. 有沒有 `<note>`？
2. `<step>` 是否和原樂譜大致一致？
3. 升降記號有沒有辨識？
4. 休止符有沒有？
5. 小節數是否合理？

然後直接把這份 MusicXML 丟進第 15 章做好的標註器。

這是第一次連上：

```text
圖片
↓
oemer
↓
MusicXML
↓
我們自己的標註器
```

但目前仍然是「手動分兩段執行」。下一章才讓 Python 自動呼叫 OMR。

---

## 實驗｜原圖與前處理圖誰比較好？

對同一張 `score_skewed.png`：

1. 直接丟 oemer。
2. 先經 `preprocess_score()`。
3. 再丟 oemer。

比較兩份 MusicXML 的：

```text
音符數
明顯錯音數
小節結構
```

這時影像處理不再只是「看起來變漂亮」，而是可以用辨識結果驗證效果。

---

## 章末檢核

1. OCR 與 OMR 差在哪裡？
2. oemer 在 ScoreSense 中的責任邊界？
3. 為什麼安裝成功後仍要人工檢查 MusicXML？
4. 如果 oemer 失敗，前面哪些功能仍然能繼續？
5. 怎麼比較前處理是否真的改善辨識？
