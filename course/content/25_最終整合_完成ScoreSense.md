# 第 25 章｜最終整合：完成 ScoreSense

這一章才真正把前面所有積木整理成最後專案。

此時看到完整資料夾，學生應該不會再覺得「怎麼突然這麼多檔案」，因為每一個核心檔案都是前面自己做過的內容。

## 學習目標

- 建立最終資料夾結構。
- 逐一核對核心模組責任。
- 從 MusicXML 與圖片兩種輸入完成 end-to-end 測試。
- 啟動 Web UI。
- 完成最終驗收清單。

[TOC]

---

## 一、最終架構

```text
ScoreSense/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── converter.py
│   │   ├── image_preprocessor.py
│   │   ├── musicxml.py
│   │   ├── omr.py
│   │   └── pipeline.py
│   └── web.py
├── data/
│   ├── uploads/
│   ├── work/
│   └── outputs/
├── samples/
│   └── twinkle.musicxml
├── static/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── tests/
│   ├── test_converter.py
│   └── test_musicxml.py
├── doctor.py
├── main.py
├── requirements.txt
└── requirements-omr.txt
```

---

## 二、學生應該能解釋每個檔案

### converter.py

```text
PitchInfo
標註模式
音名 → Do / 1 / 注音
```

### image_preprocessor.py

```text
圖片 → 灰階 → CLAHE → 估角度 → 校正 → 二值預覽
```

### omr.py

```text
Python → oemer CLI → MusicXML
```

### musicxml.py

```text
MusicXML → PitchInfo → label → 新 MusicXML
```

### pipeline.py

```text
決定前後順序與資料流
```

### web.py

```text
HTTP 輸入輸出
```

如果學生說不出其中一個檔案的責任，就回到對應章節複習。

---

## 三、第一個最終測試：不碰 OMR

```bash
python main.py process samples/twinkle.musicxml --mode zhuyin
```

確認：

```text
Job
Notes
MusicXML
Note report
```

都有出現。

這條路徑測的是：

```text
MusicXML → parser → converter → annotation → output
```

---

## 四、第二個最終測試：只測圖片前處理

```bash
python main.py preprocess path/to/score.jpg
```

確認：

```text
preprocessed.png
binary_preview.png
rotation angle
```

---

## 五、第三個最終測試：圖片完整流程

有安裝 oemer 時：

```bash
python main.py process path/to/score.jpg --mode solfege
```

資料流：

```text
圖片
↓
preprocess
↓
oemer
↓
MusicXML
↓
annotation
↓
output
```

---

## 六、第四個最終測試：Web UI

```bash
python main.py web
```

開啟：

```text
http://127.0.0.1:8000
```

依序測：

1. 上傳 `twinkle.musicxml`。
2. 選 Do Re Mi。
3. 看樂譜是否顯示。
4. 下載結果。
5. 再測 numbered。
6. 再測 zhuyin。
7. 最後才上傳圖片。

---

## 七、完整驗收清單

### 環境

- [ ] Python 版本正確。
- [ ] core requirements 可安裝。
- [ ] doctor.py 能執行。
- [ ] oemer 狀態可辨識。

### 影像

- [ ] 圖片可讀取。
- [ ] 灰階與 CLAHE 正常。
- [ ] 傾斜校正可輸出角度。
- [ ] binary preview 可產生。

### MusicXML

- [ ] 能讀 `.musicxml`。
- [ ] 能跳過 rest。
- [ ] 能處理 alter。
- [ ] 能輸出三種標註。
- [ ] 重跑不會累積 number=99。

### OMR

- [ ] command 可找到。
- [ ] log 可保存。
- [ ] 找得到輸出 MusicXML。
- [ ] 失敗時有清楚錯誤。

### Pipeline

- [ ] MusicXML 路徑可獨立運作。
- [ ] 圖片路徑可完整運作。
- [ ] 每個 job 有獨立資料夾。

### Web

- [ ] 可以上傳。
- [ ] 可以選模式。
- [ ] 可以顯示處理狀態。
- [ ] 可以顯示 MusicXML。
- [ ] 可以下載結果。

---

## 八、最重要的口頭驗收

請學生不用看程式回答：

> 「如果我上傳一張 JPG，從按下按鈕到看到注音樂譜，中間發生了什麼？」

希望能說出：

```text
前端 FormData
→ FastAPI
→ 儲存 upload
→ Pipeline
→ OpenCV 前處理
→ oemer
→ MusicXML
→ 解析 pitch
→ 轉注音
→ lyric 寫回
→ API 回傳 URL
→ 前端 fetch MusicXML
→ OSMD render
```

如果能完整說明，這個專題就不是「會 Run」而已。

---

## 九、參考專案

教材 ZIP 中的：

```text
reference_project/
```

就是最終 MVP 參考版本。

請只在學生完成各章後用來核對，不建議前期直接複製。
