# 第 10 章｜Do Re Mi、簡譜與注音轉換器

現在我們已經能用 `PitchInfo` 表示音高。接下來真正實作 ScoreSense 的核心特色：把同一顆音轉成不同標註。

這一章先採用**固定唱名**：C 永遠對應 Do／1／ㄉㄛ。

## 學習目標

- 使用 Enum 表示有限的模式選項。
- 建立三組音名對照表。
- 處理升降記號。
- 選配顯示八度提示。
- 完成 `pitch_to_label()`。

[TOC]

---

## 單元一｜三種模式其實共享同一個輸入

輸入：

```python
PitchInfo("C", 0, 4)
```

輸出可能是：

```text
Do
1
ㄉㄛ
```

因此不需要寫三套完全不同流程，只需要「不同的對照表」。

---

## 單元二｜用 Enum 限制合法模式

```python
from enum import Enum


class LabelMode(str, Enum):
    SOLFEGE = "solfege"
    NUMBERED = "numbered"
    ZHUYIN = "zhuyin"
```

好處是模式不再只是散落的任意字串。

```python
mode = LabelMode("solfege")
```

如果傳入錯誤值：

```python
LabelMode("abc")
```

會明確報錯。

---

## 單元三｜建立共用對照表

```python
BASE_LABELS = {
    LabelMode.SOLFEGE: {
        "C": "Do", "D": "Re", "E": "Mi", "F": "Fa",
        "G": "Sol", "A": "La", "B": "Si",
    },
    LabelMode.NUMBERED: {
        "C": "1", "D": "2", "E": "3", "F": "4",
        "G": "5", "A": "6", "B": "7",
    },
    LabelMode.ZHUYIN: {
        "C": "ㄉㄛ", "D": "ㄖㄟ", "E": "ㄇㄧ", "F": "ㄈㄚ",
        "G": "ㄙㄛ", "A": "ㄌㄚ", "B": "ㄒㄧ",
    },
}
```

取得：

```python
print(BASE_LABELS[LabelMode.SOLFEGE]["F"])
```

---

## 單元四｜升降記號

```python
def accidental_text(alter):
    mapping = {
        -2.0: "♭♭",
        -1.0: "♭",
        0.0: "",
        1.0: "♯",
        2.0: "𝄪",
    }
    return mapping.get(alter, f"({alter:+g})")
```

先用簡化版理解。

測試：

```python
print(accidental_text(1))
print(accidental_text(-1))
print(accidental_text(0))
```

之後可加入半升、半降。

---

## 單元五｜八度提示

這不是五線譜標準記譜，而是我們自己設計的輔助顯示：

```text
C4 → Do
C5 → Do↑
C6 → Do↑↑
C3 → Do↓
```

```python
def octave_text(octave):
    if octave is None or octave == 4:
        return ""
    if octave > 4:
        return "↑" * min(octave - 4, 3)
    return "↓" * min(4 - octave, 3)
```

---

## 單元六｜完成 pitch_to_label

```python
def pitch_to_label(
    pitch,
    mode,
    show_accidental=True,
    show_octave=False,
):
    mode = LabelMode(mode)
    step = pitch.step.upper().strip()

    if step not in BASE_LABELS[mode]:
        raise ValueError(f"不支援音名：{pitch.step}")

    base = BASE_LABELS[mode][step]
    accidental = accidental_text(pitch.alter) if show_accidental else ""
    octave = octave_text(pitch.octave) if show_octave else ""

    if mode == LabelMode.NUMBERED:
        return f"{accidental}{base}{octave}"

    return f"{base}{accidental}{octave}"
```

為什麼簡譜把升降記號放前面，而唱名放後面？

```text
♭2
Fa♯
```

這是顯示設計選擇。可以依未來需求調整。

---

## 綜合測試

```python
print(pitch_to_label(PitchInfo("C", 0, 4), "solfege"))
print(pitch_to_label(PitchInfo("F", 1, 4), "solfege"))
print(pitch_to_label(PitchInfo("D", -1, 4), "numbered"))
print(pitch_to_label(PitchInfo("B", 0, 5), "zhuyin", show_octave=True))
```

預期：

```text
Do
Fa♯
♭2
ㄒㄧ↑
```

---

## 實作練習

### 練習 A

加入：

```text
-0.5
0.5
```

的符號。

### 練習 B

如果使用者不想顯示升降記號：

```python
show_accidental=False
```

應該得到什麼？

### 練習 C

想一想：「固定唱名」與「首調唱名」差在哪裡？為什麼首調唱名不能只看 `C/D/E` 就完成？

---

## 章末檢核

1. Enum 解決什麼問題？
2. 三種模式為什麼可以共用同一個函式？
3. `PitchInfo` 是輸入還是輸出？
4. `pitch_to_label()` 應該去讀檔嗎？為什麼？
5. 首調唱名為什麼需要更多樂譜資訊？
