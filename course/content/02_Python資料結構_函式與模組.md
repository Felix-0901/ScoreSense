# 第 2 章｜Python 資料結構、函式與模組

ScoreSense 後面會遇到很多資料：一串音符、三種標註模式、每顆音的音名與八度、處理後檔案的路徑。

如果全部塞在一個變數裡，程式很快就會變亂。這一章先學會用合適的資料結構整理資訊，再把重複工作包成函式。

## 學習目標

- 使用 `list` 保存有順序的音符。
- 使用 `dict` 建立音名對照表。
- 使用函式將「輸入 → 處理 → 輸出」包起來。
- 理解參數、回傳值與區域變數。
- 建立自己的 `.py` 模組並用 `import` 使用。

[TOC]

---

## 單元一｜List：有順序的一串資料

```python
notes = ["C", "D", "E", "F", "G"]
```

這裡的順序很重要，因為樂譜上的音符本來就有先後。

```python
print(notes[0])
print(notes[-1])
print(len(notes))
```

先預測三行會印什麼。

### 逐顆處理

```python
for note in notes:
    print("目前音符：", note)
```

未來從 MusicXML 讀出來後，本質上也會做類似的事情：**一顆一顆走過去處理。**

---

## 單元二｜Dictionary：建立對照關係

固定唱名最簡單的概念是：

```text
C → Do
D → Re
E → Mi
...
```

這很適合使用字典。

```python
solfege = {
    "C": "Do",
    "D": "Re",
    "E": "Mi",
    "F": "Fa",
    "G": "Sol",
    "A": "La",
    "B": "Si",
}

print(solfege["C"])
print(solfege["F"])
```

### 練習

自己建立：

```python
numbered = {
    "C": "1",
    # 請完成
}
```

以及：

```python
zhuyin = {
    "C": "ㄉㄛ",
    # 請完成
}
```

先不要做升降記號。現在只處理最單純的七個音。

---

## 單元三｜函式：把一件工作說清楚

下面程式可以轉換音名：

```python
def to_solfege(note):
    table = {
        "C": "Do",
        "D": "Re",
        "E": "Mi",
        "F": "Fa",
        "G": "Sol",
        "A": "La",
        "B": "Si",
    }
    return table[note]

print(to_solfege("C"))
print(to_solfege("G"))
```

可以把函式想成一台小機器：

```text
輸入 note
   ↓
to_solfege()
   ↓
輸出唱名
```

### 為什麼一定要 `return`？

比較：

```python
def bad(note):
    print(note)
```

與：

```python
def good(note):
    return note
```

`print()` 是顯示；`return` 是把結果交給下一段程式。

ScoreSense 後面很多函式都要互相串接，所以「回傳資料」比「只印在畫面上」重要。

---

## 單元四｜一個函式做一件事

不好的函式可能同時：讀檔、辨識、轉換、存檔、開網頁。

一開始看起來方便，之後卻很難除錯。

我們希望函式名稱可以直接說明責任：

```text
read_image()
preprocess_score()
extract_pitch()
pitch_to_label()
annotate_musicxml()
```

這個習慣會一路用到最後的正式專案。

---

## 單元五｜建立自己的模組

建立：

```text
note_tools.py
```

```python
SOLFEGE = {
    "C": "Do",
    "D": "Re",
    "E": "Mi",
    "F": "Fa",
    "G": "Sol",
    "A": "La",
    "B": "Si",
}


def to_solfege(note):
    return SOLFEGE[note]
```

再建立：

```text
lesson02_use_module.py
```

```python
from note_tools import to_solfege

notes = ["C", "D", "E", "G"]

for note in notes:
    print(note, "→", to_solfege(note))
```

現在程式已經第一次被拆成兩個檔案。

:::info
這還不是「正式專案架構」。現在只需要理解：一個 `.py` 檔可以把功能提供給另一個 `.py` 檔使用。
:::

---

## 綜合實作｜可以切換模式的音名轉換

請先自己設計，再參考下面的方向。

```python
SOLFEGE = {
    "C": "Do", "D": "Re", "E": "Mi", "F": "Fa",
    "G": "Sol", "A": "La", "B": "Si",
}

NUMBERED = {
    "C": "1", "D": "2", "E": "3", "F": "4",
    "G": "5", "A": "6", "B": "7",
}

ZHUYIN = {
    "C": "ㄉㄛ", "D": "ㄖㄟ", "E": "ㄇㄧ", "F": "ㄈㄚ",
    "G": "ㄙㄛ", "A": "ㄌㄚ", "B": "ㄒㄧ",
}


def convert_note(note, mode):
    if mode == "solfege":
        return SOLFEGE[note]
    elif mode == "numbered":
        return NUMBERED[note]
    elif mode == "zhuyin":
        return ZHUYIN[note]
    else:
        raise ValueError("未知模式")
```

測試：

```python
print(convert_note("C", "solfege"))
print(convert_note("D", "numbered"))
print(convert_note("E", "zhuyin"))
```

### 修改練習

1. 傳入 `mode="abc"`，觀察錯誤。
2. 傳入小寫 `c`，觀察錯誤。
3. 想辦法讓 `c` 也能正常處理。

---

## 章末檢核

1. List 與 Dictionary 各適合保存什麼？
2. `print()` 和 `return` 的差別是什麼？
3. 為什麼函式不要一次做太多工作？
4. `from note_tools import to_solfege` 的意思是什麼？
5. 如果一個模式寫錯，我們希望整個程式默默繼續，還是明確報錯？為什麼？

### 本章留下的積木

```text
音名 C/D/E...
↓
字典對照
↓
函式
↓
Do/Re/Mi、1/2/3、注音
```

現在還只是「手動給音名」。之後我們要讓程式自己從 MusicXML 讀出這些音名。
