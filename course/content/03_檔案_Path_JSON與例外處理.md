# 第 3 章｜檔案、Path、JSON 與例外處理

到目前為止，資料都直接寫在程式裡。但真正專題會讀圖片、讀 MusicXML、產生新檔案、保存處理結果。

因此在碰影像之前，先建立「檔案系統」觀念。

## 學習目標

- 使用 `pathlib.Path` 處理檔案與資料夾。
- 讀寫文字檔與 JSON。
- 使用 `try / except` 處理可預期錯誤。
- 理解「檢查輸入」為什麼是系統的一部分。
- 建立自己的 `input/` 與 `output/` 練習流程。

[TOC]

---

## 單元一｜路徑其實也是資料

建立：

```python
from pathlib import Path

path = Path("materials") / "tiny_score.musicxml"

print(path)
print("檔名：", path.name)
print("副檔名：", path.suffix)
print("存在嗎：", path.exists())
```

`/` 在這裡不是除法，而是 `Path` 提供的路徑組合方式。

這比手動寫：

```python
"materials/tiny_score.musicxml"
```

更容易跨 Windows、macOS 與 Linux。

---

## 單元二｜建立輸出資料夾

```python
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

print(output_dir.resolve())
```

`exist_ok=True` 的意思是：資料夾已存在也不用報錯。

後面的 ScoreSense 會大量使用這種方式建立工作目錄。

---

## 單元三｜讀文字檔

先建立 `hello.txt`：

```text
C4
D4
E4
```

再讀取：

```python
from pathlib import Path

path = Path("hello.txt")
text = path.read_text(encoding="utf-8")
print(text)
```

寫入：

```python
Path("output/result.txt").write_text("Do Re Mi", encoding="utf-8")
```

### 練習

把：

```python
notes = ["C4", "D4", "E4"]
```

用換行組成文字後寫入檔案。

提示：

```python
"\n".join(notes)
```

---

## 單元四｜JSON：讓資料保留結構

文字檔很容易看，但如果每顆音符除了音名，還要保存八度、升降記號、標註，就需要更有結構的格式。

```python
notes = [
    {"step": "C", "octave": 4, "label": "Do"},
    {"step": "F", "octave": 4, "alter": 1, "label": "Fa♯"},
]
```

寫成 JSON：

```python
import json
from pathlib import Path

Path("output/notes.json").write_text(
    json.dumps(notes, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
```

打開檔案觀察：

```json
[
  {
    "step": "C",
    "octave": 4,
    "label": "Do"
  }
]
```

後面的完整專案也會輸出 `notes.json`，方便除錯與檢查。

---

## 單元五｜錯誤不是敵人，而是資訊

如果程式讀一個不存在的檔案：

```python
Path("not_found.txt").read_text()
```

會得到 `FileNotFoundError`。

可以先檢查：

```python
path = Path("not_found.txt")

if not path.exists():
    print("檔案不存在")
```

也可以使用：

```python
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    print("找不到檔案：", path)
```

:::warning
不要一看到錯誤就寫 `except Exception: pass`。那會把真正的問題藏起來。除錯時需要知道「哪一步錯、為什麼錯」。
:::

---

## 單元六｜副檔名檢查

ScoreSense 最後會接受圖片與 MusicXML，但不能什麼檔案都處理。

```python
from pathlib import Path

path = Path("music.jpg")
suffix = path.suffix.lower()

if suffix in {".jpg", ".jpeg", ".png"}:
    print("這是支援的圖片")
elif suffix in {".xml", ".musicxml", ".mxl"}:
    print("這是樂譜資料")
else:
    print("不支援")
```

這是後面 Pipeline 判斷「接下來走 OMR 還是直接讀 MusicXML」的基礎。

---

## 綜合實作｜建立一個安全的小檔案處理器

建立 `lesson03_file_checker.py`：

```python
from pathlib import Path


def inspect_file(filename):
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"找不到：{path}")

    suffix = path.suffix.lower()

    if suffix in {".png", ".jpg", ".jpeg"}:
        kind = "image"
    elif suffix in {".xml", ".musicxml", ".mxl"}:
        kind = "score"
    else:
        kind = "unsupported"

    return {
        "name": path.name,
        "suffix": suffix,
        "kind": kind,
    }
```

請拿 `materials/tiny_score.musicxml` 測試。

### 修改練習

1. 加入 `.webp`。
2. 讓 `.PDF` 轉成小寫後能判斷。
3. 如果是不支援格式，改成 `raise ValueError(...)`。

---

## 章末檢核

1. 為什麼專案不建議到處直接拼字串路徑？
2. `Path.mkdir()` 的用途是什麼？
3. JSON 比純文字適合保存哪類資料？
4. `try / except` 應該拿來隱藏錯誤嗎？
5. 為什麼上傳檔案後要先檢查副檔名？

下一章開始正式進入影像資料。
