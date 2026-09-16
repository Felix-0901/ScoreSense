# 第 15 章｜里程碑一：完成 MusicXML 自動標註器

這一章不新增太多新知，而是把第 9～14 章整合成第一個真正可以展示的小作品。

**輸入不再是圖片，而是一份 MusicXML。**

這樣學生可以先確認最核心的「音符分析與標註」完全正確，再加入 OMR。

## 學習目標

- 將 `PitchInfo`、轉換器與 MusicXML parser 串接。
- 建立簡單主程式。
- 讓使用者選擇三種模式。
- 產生新 MusicXML 與 notes.json。
- 使用輸入／輸出案例做人工驗證。

[TOC]

---

## 一、目前已有的積木

```text
PitchInfo
    ↓
pitch_to_label()
    ↓
XML parser
    ↓
extract_pitch()
    ↓
annotate_musicxml()
```

現在缺的是一個「主程式」決定它們怎麼被使用。

---

## 二、先建立簡單主程式，不用 argparse

建立：

```text
milestone1.py
```

```python
from pathlib import Path

from converter import LabelMode
from musicxml_tools import annotate_musicxml, save_note_report


input_path = Path("materials/twinkle.musicxml")
output_dir = Path("output/milestone1")
output_dir.mkdir(parents=True, exist_ok=True)

mode = input("模式 solfege / numbered / zhuyin：").strip()

if mode not in {m.value for m in LabelMode}:
    raise ValueError("模式錯誤")

output_xml = output_dir / f"annotated_{mode}.musicxml"
notes = annotate_musicxml(
    input_path,
    output_xml,
    mode,
)

save_note_report(notes, output_dir / "notes.json")

print("完成")
print("音符數量：", len(notes))
print("輸出：", output_xml)
```

這裡如果你的檔名不同，請依自己的教材實作調整 import。

---

## 三、驗收三種模式

分別輸入：

```text
solfege
numbered
zhuyin
```

應得到三個 MusicXML。

請不要一次跑完就算通過，每一份都至少抽查前 5 顆音。

建立表格：

| 原音 | solfege | numbered | zhuyin |
| --- | --- | --- | --- |
| C4 | Do | 1 | ㄉㄛ |
|  |  |  |  |

---

## 四、測試升降記號

使用含 F♯ 的 `tiny_score.musicxml`。

確認：

```text
F + alter=1
```

在三種模式是否得到預期結果。

---

## 五、測試休止符

計算：

```text
XML 中 note 總數
實際標註音符數
```

如果 XML 有 rest，兩者不應該一定相同。

學生要能說出原因。

---

## 六、第一次做「功能驗收」

### 驗收條件

- [ ] 能讀 `.musicxml`。
- [ ] 能取得 pitched notes。
- [ ] rest 不會產生假 label。
- [ ] 能輸出 Do Re Mi。
- [ ] 能輸出 1 2 3。
- [ ] 能輸出注音。
- [ ] 升降記號可顯示。
- [ ] 標註會寫回新的 MusicXML。
- [ ] 原檔不被覆蓋。
- [ ] notes.json 可查看處理結果。

---

## 七、這個里程碑為什麼重要？

如果下一階段 OMR 辨識錯，我們現在能分清楚：

```text
問題 A：OMR 把音認錯
```

還是：

```text
問題 B：我們的 MusicXML 解析／標註程式寫錯
```

因為 B 已經先被單獨驗證。

這是大型專案很重要的拆解方式。

---

## 章末任務

請學生不用看程式，畫出：

```text
MusicXML
↓
哪個函式？
↓
PitchInfo
↓
哪個函式？
↓
label
↓
哪個函式？
↓
新 MusicXML
```

如果畫得出來，才進 OMR。
