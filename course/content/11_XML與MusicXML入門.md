# 第 11 章｜XML 與 MusicXML 入門

到目前為止，我們都手動建立 `PitchInfo`。真正系統需要從樂譜資料中取得音符。

在加入 OMR 前，先弄懂 OMR 最後會交給我們的東西：**MusicXML**。

## 學習目標

- 理解 XML 是「有階層的文字資料」。
- 看懂標籤、屬性、父子結構。
- 認識 MusicXML 中的 score、part、measure、note、pitch。
- 從 XML 片段中人工找出 C4、F♯4 與休止符。
- 理解為什麼先學輸出格式，再學 OMR。

[TOC]

---

## 單元一｜XML 不是程式碼

XML 是一種文字格式，用標籤描述資料結構。

```xml
<student>
  <name>Amy</name>
  <score>90</score>
</student>
```

可以讀成：

```text
student
├── name = Amy
└── score = 90
```

---

## 單元二｜元素、文字與屬性

```xml
<measure number="1">
  ...
</measure>
```

`measure` 是元素名稱。

`number="1"` 是屬性。

如果：

```xml
<step>C</step>
```

文字 `C` 是元素內容。

---

## 單元三｜一顆音在 MusicXML 裡可能長這樣

```xml
<note>
  <pitch>
    <step>F</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
  <duration>1</duration>
  <type>quarter</type>
</note>
```

現在不用寫 Python，直接人工解讀：

```text
step   = F
alter  = 1
odtave = 4
```

所以是：

```text
F♯4
```

這正好可以轉成：

```python
PitchInfo("F", 1, 4)
```

---

## 單元四｜休止符

```xml
<note>
  <rest/>
  <duration>1</duration>
</note>
```

這顆 note 沒有 `<pitch>`。

因此我們的 parser 之後必須先問：

```text
這是休止符嗎？
```

不能假設每個 `<note>` 都有音高。

---

## 單元五｜樂譜有層級

簡化結構：

```text
score-partwise
└── part
    ├── measure 1
    │   ├── note
    │   ├── note
    │   └── note
    └── measure 2
        ├── note
        └── note
```

所以我們最後要做的是：

```text
走遍所有 note
↓
如果有 pitch
↓
取 step / alter / octave
```

---

## 單元六｜打開教材檔人工觀察

打開：

```text
materials/tiny_score.musicxml
```

先不要執行程式。

請找出：

1. 第一顆有音高的 note 是什麼？
2. 有沒有休止符？
3. 哪一顆音有 `<alter>`？
4. `<measure number="1">` 表示什麼？

---

## 單元七｜為什麼 OMR 要晚一點學？

如果第一天只執行：

```text
圖片 → oemer → 一個 XML 檔
```

學生可能只知道「工具生出一個檔」。

但現在我們知道：

```text
OMR 的價值
=
把圖片轉成結構化樂譜資料
```

而且知道之後真正要取的是：

```text
<step>
<alter>
<octave>
```

所以 OMR 不再是黑盒子魔法，而是一個「輸入轉換器」。

---

## 小練習｜自己手寫 MusicXML 片段

請寫出：

```text
C4 四分音符
D4 四分音符
一個休止符
F#4 四分音符
```

只要求 `<note>` 片段即可，不必完整 MusicXML。

---

## 章末檢核

1. XML 的層級是什麼意思？
2. `<step>`、`<alter>`、`<octave>` 分別代表什麼？
3. 為什麼休止符不能照一般音符解析？
4. OMR 的輸出 MusicXML 對後續程式有什麼價值？
5. 為什麼我們先學 MusicXML 再學 oemer？
