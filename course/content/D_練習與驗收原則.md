# 練習與驗收原則

這份教材不建議把每一個練習都變成「照著完整答案打一遍」。

## 一、四種練習層級

### 1. 預測

執行前先回答輸出或 shape。

目的：確認不是只靠 trial and error。

### 2. 修改

只改一個參數或一小段邏輯。

目的：看學生是否知道哪個部分控制結果。

### 3. 補完

提供函式框架，學生完成中間邏輯。

目的：開始自己組織程式。

### 4. 里程碑

只提供需求與資料流，不逐行給答案。

目的：檢查能否把前面積木組起來。

---

## 二、建議不要直接給答案的章節

尤其：

```text
10 pitch_to_label
13 extract_pitch
14 annotate_musicxml
18 end-to-end 串接
20 process_file
```

可以先讓學生做，再用 reference project 比對。

---

## 三、口頭驗收比背語法重要

學生不需要背：

```python
cv2.ADAPTIVE_THRESH_GAUSSIAN_C
```

但要知道：

> 為什麼光線不均時，局部 threshold 可能比固定 threshold 合適？

同樣，學生不必背 ElementTree 每個 API，但要知道：

> MusicXML 的 `<note>` 裡，哪幾個元素可以組成 PitchInfo？

---

## 四、最後的最低理解標準

學生應能畫出並口頭解釋：

```text
JPG
→ OpenCV
→ oemer
→ MusicXML
→ PitchInfo
→ label
→ lyric
→ FastAPI
→ OSMD
```

如果只會說「按 Run 就會出結果」，表示專題理解仍不足。
