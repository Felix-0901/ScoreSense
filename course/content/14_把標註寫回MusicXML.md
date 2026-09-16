# 第 14 章｜把標註寫回 MusicXML

現在程式已經知道每顆音的 label，但使用者真正需要的是：**標註出現在樂譜上。**

本章採用 MusicXML 的 `<lyric>` 元素加入一條新的標註線。

## 學習目標

- 理解「修改 XML 樹」與「重新輸出檔案」。
- 使用 `ET.Element` 與 `ET.SubElement` 新增元素。
- 保留既有歌詞，不覆蓋使用者資料。
- 使用固定 lyric number 管理系統標註。
- 完成 `annotate_musicxml()`。

[TOC]

---

## 單元一｜我們不直接畫字在 PNG 上

為什麼不直接在原圖的音符下面用 OpenCV `putText()`？

因為你要知道每顆音符在圖片上的精確版面座標，而且換行、縮放、不同樂譜版面會很麻煩。

MusicXML 本身已經有「樂譜結構」。我們把標註放回資料裡，再交給樂譜顯示工具排版，會更合理。

---

## 單元二｜要加入什麼 XML？

例如：

```xml
<lyric number="99" color="#C62828">
  <syllabic>single</syllabic>
  <text>Do</text>
</lyric>
```

我們選 `number="99"` 當作 ScoreSense 自己的標註線。

這樣原本的：

```xml
<lyric number="1">...</lyric>
```

不會被覆蓋。

---

## 單元三｜建立新元素

```python
lyric = ET.Element("lyric", {
    "number": "99",
    "color": "#C62828",
})

syllabic = ET.SubElement(lyric, "syllabic")
syllabic.text = "single"

text = ET.SubElement(lyric, "text")
text.text = "Do"

note.append(lyric)
```

這就是「修改 XML 樹」。

---

## 單元四｜避免重跑後一直累積

如果使用者第一次產生 Do，第二次改成 1，我們不希望同一顆 note 底下出現：

```text
Do
1
ㄉㄛ
```

所以先刪除自己上一輪的 `number=99`。

```python
for lyric in list(children(note, "lyric")):
    if lyric.attrib.get("number") == "99":
        note.remove(lyric)
```

這是「可重複執行」的重要設計。

---

## 單元五｜namespace 不能忘記

如果原始 XML 使用 namespace，新建立元素最好跟著相同 namespace。

```python
def namespace_prefix(tag):
    if tag.startswith("{"):
        return tag.split("}", 1)[0] + "}"
    return ""
```

使用：

```python
namespace = namespace_prefix(root.tag)

lyric = ET.Element(f"{namespace}lyric", {"number": "99"})
```

---

## 單元六｜核心迴圈

```python
results = []
index = 0

for note in iter_by_local_name(root, "note"):
    pitch = extract_pitch(note)

    if pitch is None:
        continue

    index += 1
    label = pitch_to_label(pitch, "solfege")

    # 移除舊的 number=99
    # 建立新的 lyric
    # append 回 note
```

---

## 單元七｜寫出新 MusicXML

```python
from pathlib import Path

output_path = Path("output/annotated.musicxml")
output_path.parent.mkdir(parents=True, exist_ok=True)

ET.indent(tree, space="  ")
tree.write(
    output_path,
    encoding="utf-8",
    xml_declaration=True,
)
```

原始檔不要直接覆蓋，教學期間先永遠輸出新檔案。

---

## 綜合實作｜完成 annotate_musicxml

函式設計：

```python
def annotate_musicxml(
    input_path,
    output_path,
    mode,
    show_accidental=True,
    show_octave=False,
):
    ...
    return results
```

輸入：

```text
materials/twinkle.musicxml
```

輸出：

```text
output/annotated_solfege.musicxml
```

以及 Python 內的 `results` 音符資料。

---

## 驗證方式

不要只看「檔案有出現」。

請打開輸出 XML 搜尋：

```text
number="99"
```

確認：

1. pitched note 有新增標註。
2. rest 沒有被硬加音高標註。
3. 重新執行不會累積多條 99。
4. 原始 lyric number 1 如果存在仍保留。

---

## 章末檢核

1. 為什麼使用 lyric，而不是直接把字畫到圖片？
2. `number="99"` 的用途是什麼？
3. 為什麼重跑前先刪掉舊 99？
4. 為什麼輸出到新檔而不是直接改原始檔？
5. namespace 在新增 XML 元素時為什麼重要？
