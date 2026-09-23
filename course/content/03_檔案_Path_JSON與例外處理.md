# 第 3 章｜檔案、Path、JSON 與例外處理

第 2 章的程式將資料直接寫在變數裡。程式結束後，記憶體中的資料不會自動保存；每次需要換一組資料，也得修改程式。

本章會將「程式」與「資料」分開：從檔案讀取內容，檢查資料，完成運算，再將結果寫入另一個檔案。

## 學習目標

- 分辨檔案、資料夾、相對路徑與絕對路徑。
- 使用 `pathlib.Path` 組合路徑與查詢檔案資訊。
- 使用 UTF-8 讀寫文字，理解讀取、覆寫、附加與建立新檔的差異。
- 將 Python 資料轉成 JSON，並正確讀回。
- 閱讀錯誤訊息，使用 `try / except / else / finally`。
- 使用 `raise` 表達無法接受的輸入。
- 完成保留輸入原檔、具有資料驗證的成績報告程式。

[TOC]

---

## 單元一｜檔案、資料夾與路徑

### 1-1｜資料保存在什麼地方？

檔案保存內容，資料夾用來整理檔案。路徑則描述檔案或資料夾的位置。

本章的練習使用以下結構，程式檔都放在 `scoresense_course` 根目錄：

```text
scoresense_course/
├── prepare_lesson03.py
├── lesson03_paths.py
├── lesson03_report.py
└── lesson03_data/
    ├── input/
    │   ├── message.txt
    │   ├── scores.txt
    │   └── students.json
    └── output/
```

`input` 保存輸入資料，`output` 保存產生的結果。處理資料時，不必把新結果寫回原始輸入檔。

除非範例另外指定檔名，每個 Python 程式區塊可以各存成根目錄的一支練習程式，例如 `lesson03_practice.py`，再執行觀察。讀取練習素材的範例，需要先完成單元三的素材準備。

### 1-2｜相對路徑與絕對路徑

`lesson03_data/input/message.txt` 是相對路徑，需要一個起點才能找到檔案。

絕對路徑則從作業系統的根位置開始，例如 Windows 的磁碟機路徑，或 macOS、Linux 以 `/` 開頭的路徑。每台電腦的使用者名稱與資料夾位置可能不同，因此不適合把自己電腦的完整路徑寫死在所有程式裡。

### 1-3｜目前工作目錄不是程式所在目錄

建立 **`lesson03_paths.py`**：

```python
from pathlib import Path

print("目前工作目錄：", Path.cwd())
print("程式所在目錄：", Path(__file__).resolve().parent)
```

`Path.cwd()` 是程式執行時的工作目錄，會受到終端機位置與啟動方式影響。

`__file__` 表示目前這個 Python 檔案的路徑。`.resolve()` 取得解析後的絕對路徑，`.parent` 取得所在資料夾。

因此：

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"

print(path)
```

這個寫法以程式檔的位置為基準，不是依賴終端機剛好開在哪裡。

`__file__` 適用於存成 `.py` 的程式；互動式 Python 或 Notebook 通常沒有這個名稱。若在互動環境練習，可明確選擇 `Path.cwd()` 作為基準，但要先確認目前位置。

### 小實驗

先從專案根目錄執行 `lesson03_paths.py`，再從上一層以 `python scoresense_course/lesson03_paths.py` 執行。比較兩次的工作目錄與程式所在目錄。

---

## 單元二｜使用 `Path` 處理路徑

### 2-1｜建立路徑物件

```python
from pathlib import Path

path = Path("lesson03_data") / "input" / "message.txt"

print(path.as_posix())
print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent.as_posix())
```

輸出：

```text
lesson03_data/input/message.txt
message.txt
message
.txt
lesson03_data/input
```

`Path` 物件保存路徑資訊。`/` 在這裡用來組合路徑，不是做除法。`.as_posix()` 以正斜線顯示路徑，方便跨平台比較文字結果。

建立 `Path(...)` 不會建立實際檔案，`.with_name()` 與 `.with_suffix()` 也只會產生新的路徑物件。

```python
from pathlib import Path

path = Path("output") / "report.txt"
new_path = path.with_suffix(".json")

print(path.as_posix())
print(new_path.as_posix())
```

這段程式不會把文字內容轉換成 JSON，也不會替磁碟上的檔案改名。

### 2-2｜檢查存在與類型

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"

print("存在：", path.exists())
print("是檔案：", path.is_file())
print("是資料夾：", path.is_dir())
```

完成素材準備後，這三行應分別顯示 `True`、`True`、`False`。

`exists()` 為真，不代表它一定是檔案，也不代表一定有讀取權限。真正讀檔時仍可能發生錯誤。

### 2-3｜建立資料夾

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "lesson03_data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)

print(output_dir.is_dir())
```

`parents=True` 會一併建立缺少的上層資料夾。`exist_ok=True` 允許目標資料夾已經存在；如果同名位置是一般檔案，仍會報錯。

`.resolve()` 是路徑解析，不是建立資料夾。寫入檔案前，需要的父資料夾必須已存在。

### 2-4｜Windows 路徑與反斜線

Python 字串中的反斜線可能形成跳脫字元，例如 `\n` 是換行。

手動輸入 Windows 路徑時，可以使用 raw string，如 `r"C:\Users\Student\Documents"`，或使用正斜線。更一般的做法是由 `BASE_DIR` 配合 `/` 組合子路徑。

`Path` 會依目前作業系統解讀路徑，不代表 Windows 的磁碟機路徑能直接在 macOS 上使用。

---

## 單元三｜準備練習資料

建立 **`prepare_lesson03.py`**，放在 `scoresense_course` 根目錄。

下面程式會準備三份小型資料。它使用 `"x"` 模式建立新檔，已存在的同名檔案會保留，不覆蓋自行修改過的內容。

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "lesson03_data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

samples = {
    "message.txt": "今天學習檔案讀寫。\nPython 可以處理文字資料。\n",
    "scores.txt": "82\n91\n58\n69\n",
    "students.json": """[
  {"name": "小安", "score": 82},
  {"name": "小晴", "score": 91},
  {"name": "小宇", "score": 58},
  {"name": "小庭", "score": 69}
]
""",
}

for filename, content in samples.items():
    path = INPUT_DIR / filename
    try:
        with path.open("x", encoding="utf-8") as file:
            file.write(content)
    except FileExistsError:
        print(f"保留既有檔案：{filename}")
    else:
        print(f"建立：{filename}")
```

在根目錄執行 `python prepare_lesson03.py`，第一次會建立資料，再執行則顯示保留既有檔案。

這裡的 `with` 用來管理檔案開關，`try / except` 處理同名檔已存在的情況，後面的單元會分別說明。

---

## 單元四｜文字、編碼與讀取檔案

### 4-1｜文字需要編碼

磁碟上的檔案保存位元組。讀取文字時，程式需要依指定編碼，將位元組解讀成字串。

本章的文字檔與 JSON 都使用 UTF-8，讀寫時明確指定 `encoding="utf-8"`，避免不同系統的預設編碼造成差異。

```python
text = "你好"
data = text.encode("utf-8")

print(len(text))
print(len(data))
print(data.decode("utf-8"))
```

輸出：

```text
2
6
你好
```

在這個例子中，兩個中文字使用六個 UTF-8 位元組。字串長度與檔案位元組數不是同一件事。

### 4-2｜一次讀取整份文字

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"
text = path.read_text(encoding="utf-8")

print(text, end="")
print(type(text).__name__)
```

`read_text()` 回傳字串，讀取完成後會關閉檔案。上例的檔案內容已含換行，所以用 `end=""` 避免額外多印一個換行。

### 4-3｜使用 `with open()`

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"

with path.open("r", encoding="utf-8") as file:
    text = file.read()

print(text, end="")
print("已關閉：", file.closed)
```

`"r"` 表示讀取。`as file` 將開啟的檔案物件交給名稱 `file` 使用。

離開 `with` 區塊時，檔案會被關閉，即使區塊中發生例外也一樣。讀到的 `text` 仍可使用，但不能再從已關閉的 `file` 讀取。

### 4-4｜逐行讀取

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"

with path.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        print(f"第 {line_number} 行：{line.rstrip()}")
```

走訪檔案物件會逐行取得文字，不必先把整份檔案讀成大字串。

`.rstrip()` 會移除結尾空白；這個例子用於顯示。需要保留結尾空格的資料時，不能隨意套用它。

### 4-5｜`read()`、`readline()` 與 `readlines()`

| 方法 | 回傳內容 |
| --- | --- |
| `read()` | 從目前位置讀到結尾，回傳字串 |
| `readline()` | 讀取一行，回傳字串 |
| `readlines()` | 讀取剩餘所有行，回傳字串串列 |

檔案有目前讀取位置，不會每次呼叫都自動回到開頭。

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"

with path.open("r", encoding="utf-8") as file:
    first = file.readline()
    remaining = file.read()
    at_end = file.read()

print(repr(first))
print(repr(remaining))
print(repr(at_end))
```

最後一行會是 `''`，表示已經讀到結尾。`repr()` 讓換行等字元以 `\n` 的形式顯示，方便檢查。

### 小練習

逐行讀取 `message.txt`，輸出行號與每行的文字長度。先決定長度是否包含換行字元，再檢查結果是否符合自己的定義。

---

## 單元五｜寫入、覆寫、附加與建立新檔

### 5-1｜常用模式

| 模式 | 用途 | 檔案已存在時 |
| --- | --- | --- |
| `"r"` | 讀取 | 從開頭讀取，不修改內容 |
| `"w"` | 寫入 | 開啟時先清空原有內容 |
| `"a"` | 附加 | 在原內容結尾繼續寫入 |
| `"x"` | 只建立新檔 | 發生 `FileExistsError` |

`"w"` 與 `"a"` 在檔案不存在時會建立檔案，但不會自動建立父資料夾。`"r"` 遇到不存在的檔案會發生 `FileNotFoundError`。

### 5-2｜寫入處理結果

下面只覆寫練習產生的 `output/summary.txt`，不改動 `input` 中的檔案。

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "lesson03_data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)

path = output_dir / "summary.txt"
text = "人數：4\n平均：75.00\n"
written = path.write_text(text, encoding="utf-8")

print("寫入字元數：", written)
print(path.read_text(encoding="utf-8"), end="")
```

`write_text()` 會覆寫同名檔案，回傳寫入的字元數，不是位元組數。需要保留舊版本時，改用新檔名或 `"x"` 模式。

### 5-3｜附加文字

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "lesson03_data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)

with (output_dir / "practice.log").open("a", encoding="utf-8") as file:
    file.write("完成一次讀寫練習\n")
```

每執行一次就增加一行，不會清空舊內容。`write()` 不會自動加入換行，必須自行放入 `\n`。

### 5-4｜只允許建立新檔

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "lesson03_data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)
path = output_dir / "first_note.txt"

try:
    with path.open("x", encoding="utf-8") as file:
        file.write("這份檔案不會被同一段範例覆蓋。\n")
except FileExistsError:
    print("檔案已存在，請使用新的檔名")
else:
    print("新檔建立完成")
```

先檢查 `exists()` 再用 `"w"` 寫入，兩步之間仍可能有其他程式建立檔案。`"x"` 將「必須不存在」交給開啟檔案的操作一起檢查。

這不代表整次寫入一定能完成；磁碟空間或其他 I/O 錯誤仍可能造成不完整的輸出。

### 5-5｜將多筆文字組成檔案內容

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "lesson03_data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)

names = ["小安", "小晴", "小宇"]
text = "\n".join(names) + "\n"
(output_dir / "names.txt").write_text(text, encoding="utf-8")
```

`"\n".join(names)` 在項目之間加換行，最後另外加一個 `\n`，讓最後一行也以換行結束。

---

## 單元六｜文字模式與二進位模式

文字模式處理 `str`，二進位模式處理 `bytes`。

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "message.txt"

text = path.read_text(encoding="utf-8")
data = path.read_bytes()

print(type(text).__name__)
print(type(data).__name__)
print("位元組數：", len(data))
```

`read_bytes()` 不進行文字解碼。也可以用 `path.open("rb")` 讀取位元組，用 `"wb"` 寫入；二進位模式不能指定 `encoding`。

圖片、壓縮檔等不能當成 UTF-8 文字直接讀寫。即使成功取得圖片的位元組，也還沒有得到像素陣列，需要影像函式庫進一步解碼。

---

## 單元七｜從文字取得數值資料

### 7-1｜拆行、清理與轉型

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "scores.txt"
text = path.read_text(encoding="utf-8")
scores = []

for line in text.splitlines():
    cleaned = line.strip()
    if not cleaned:
        continue
    scores.append(int(cleaned))

print(scores)

if scores:
    print(f"平均：{sum(scores) / len(scores):.2f}")
else:
    print("沒有分數")
```

預期輸出：

```text
[82, 91, 58, 69]
平均：75.00
```

`.splitlines()` 拆分不同形式的換行。這個版本明確略過空白行，但要求其餘每一行都能轉成整數。

### 7-2｜格式錯誤與資料不合理是兩回事

`abc` 不是整數文字，`int()` 無法轉換。`105` 可以轉成整數，但超過一般百分制的範圍。

因此讀到數值之後，還需要檢查用途所要求的條件。

```python
score = 105

if not 0 <= score <= 100:
    print("分數必須介於 0 到 100")
else:
    print("分數有效")
```

不要把無法解析的內容直接當成零，否則「資料錯誤」會變成一筆看起來正常的零分。

### 小練習

複製 `scores.txt` 為 `scores_practice.txt`，加入空白行、`abc` 與 `105`，觀察不同問題發生在哪一步。保留原本的 `scores.txt`，供後面正常範例使用。

---

## 單元八｜JSON：保存資料結構

### 8-1｜為什麼不只存純文字？

只有一串分數時，每行一個數字很容易處理。但如果每筆資料同時包含姓名、分數、狀態與多個標籤，就需要能表達結構的格式。

JSON 本身仍是文字格式，但用物件、陣列與基本值描述資料結構。

```json
{
  "name": "小安",
  "score": 82,
  "passed": true,
  "tags": ["Python", "練習"],
  "remark": null
}
```

### 8-2｜Python 與 JSON 的對照

| Python | JSON | 說明 |
| --- | --- | --- |
| `dict` | object | JSON 的鍵使用雙引號字串 |
| `list` | array | 有順序的多個項目 |
| `str` | string | 字串使用雙引號 |
| `int`、`float` | number | 不用引號包住數字 |
| `True`、`False` | `true`、`false` | 大小寫不同 |
| `None` | `null` | 表示沒有值 |

JSON 不接受一般註解、單引號字串或最後一項後面的多餘逗號。

Python 字典不等於 JSON 文字。`str(data)` 只是 Python 的文字表示，不應拿來當作正式 JSON 輸出。

### 8-3｜`dumps()`：資料轉成 JSON 字串

```python
import json

student = {
    "name": "小安",
    "score": 82,
    "passed": True,
    "remark": None,
}

text = json.dumps(student, ensure_ascii=False, indent=2, allow_nan=False)
print(text)
print(type(text).__name__)
```

`ensure_ascii=False` 讓中文字直接顯示，`indent=2` 使用兩個空格縮排，`allow_nan=False` 不允許輸出 JSON 標準不接受的 `NaN`、`Infinity` 等值。

`dumps()` 只產生字串，不會自動建立檔案。

### 8-4｜`loads()`：JSON 字串轉回資料

```python
import json

text = '{"name": "小安", "score": 82, "passed": true}'
student = json.loads(text)

print(type(student).__name__)
print(student["name"])
print(student["score"] + 5)
print(student["passed"])
```

輸出：

```text
dict
小安
87
True
```

JSON 最外層也可以是陣列、字串、數字或 `null`，所以解析成功不保證一定得到字典。

### 8-5｜不能直接保存的型別

Tuple 寫成 JSON 時會變成陣列，讀回來通常是 `list`，不會自動恢復成 tuple。

`set`、`Path` 與一般自訂物件不能直接由預設 JSON 編碼器保存。需要先明確轉成可表示的資料，例如集合轉成排序後的串列，路徑轉成字串。

```python
import json
from pathlib import Path

data = {
    "tags": sorted({"Python", "JSON"}),
    "path": (Path("output") / "report.json").as_posix(),
}

print(json.dumps(data, ensure_ascii=False, indent=2))
```

不應使用 `eval()` 將 JSON 文字當成 Python 程式執行；讀取 JSON 使用 `json.loads()` 或 `json.load()`。

---

## 單元九｜JSON 檔案讀寫

### 9-1｜字串介面與檔案介面

| 函式 | 輸入與用途 |
| --- | --- |
| `json.dumps(data)` | 將資料轉成 JSON 字串 |
| `json.loads(text)` | 將 JSON 字串轉成 Python 資料 |
| `json.dump(data, file)` | 將 JSON 寫入已開啟的檔案 |
| `json.load(file)` | 從已開啟的檔案讀取 JSON |

名稱後面的 `s` 可以記成字串介面。`loads("students.json")` 不會讀取同名檔案，而是把 `students.json` 這段文字當成 JSON 解析。

### 9-2｜讀取 JSON 檔案

```python
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "students.json"

with path.open("r", encoding="utf-8") as file:
    students = json.load(file)

for student in students:
    print(f"{student['name']}：{student['score']}")
```

這裡依照準備好的素材格式走訪資料。對不熟悉的外部資料，應先驗證最外層與每筆內容，再取用欄位。

### 9-3｜寫入新的結果檔

這個範例的 `settings.json` 是練習輸出，重跑會更新同名檔內容。

```python
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "lesson03_data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)

settings = {
    "title": "成績摘要",
    "pass_score": 60,
    "show_names": True,
}
path = output_dir / "settings.json"

with path.open("w", encoding="utf-8") as file:
    json.dump(settings, file, ensure_ascii=False, indent=2, allow_nan=False)
    file.write("\n")

with path.open("r", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded == settings)
```

最後輸出 `True`，表示這組資料寫入再讀回後，內容相等。

### 9-4｜不要將多份 JSON 直接附加在一起

同一個 JSON 檔案通常是一個完整 JSON 值。將 `{"a": 1}` 與 `{"b": 2}` 直接前後附加，不會自動變成合法的 JSON 陣列。

需要保存多筆資料時，先用串列組成一個 JSON 陣列再寫入，或明確選擇其他格式；不要只是對 JSON 檔使用 `"a"`。

### 小練習

建立含有 `title`、`items`、`completed` 三個欄位的字典，將它存成 JSON 再讀回。確認中文字、串列與布林值都保留正確型別。

---

## 單元十｜閱讀錯誤訊息

### 10-1｜三種常見問題

**語法錯誤**：程式不符合 Python 的文法，例如缺少冒號或縮排不正確。程式可能尚未開始執行就被拒絕。

**執行時例外**：語法正確，但執行某一步時無法完成，例如檔案不存在、文字不能轉成數字、除以零。

**邏輯錯誤**：程式可以執行，卻得到不符合需求的答案。例如把及格條件寫成 `score > 60`，使 `60` 被判斷成不及格。

`try / except` 處理的是執行過程中的例外，不會自動找出所有邏輯錯誤，也不能修好同一份檔案中讓程式無法解析的語法錯誤。

### 10-2｜Traceback 怎麼看？

以下是將 `abc` 轉成整數時的錯誤示意，行號依實際檔案而異：

```text
Traceback (most recent call last):
  File "lesson03_example.py", line 2, in <module>
    score = int(text)
ValueError: invalid literal for int() with base 10: 'abc'
```

先看最後一行的例外型別與原因，再向上找到自己程式中的檔名、行號與操作。

需要檢查資料時，可以暫時加入 `print(repr(text))` 與 `print(type(text).__name__)`。`repr()` 能顯示前後空白與換行，避免只靠畫面猜內容。

### 10-3｜常見例外

| 例外 | 常見情況 |
| --- | --- |
| `FileNotFoundError` | 檔案或需要的父資料夾不存在 |
| `FileExistsError` | 使用 `"x"` 建立已存在的檔案 |
| `PermissionError` | 沒有讀寫權限 |
| `IsADirectoryError` | 將資料夾當成一般檔案操作 |
| `UnicodeDecodeError` | 內容無法用指定編碼解讀 |
| `json.JSONDecodeError` | 文字不是可解析的 JSON |
| `ValueError` | 值不符合要求 |
| `TypeError` | 型別或呼叫方式不符合要求 |
| `KeyError` | 字典缺少指定鍵 |
| `ZeroDivisionError` | 除以零 |

具體檔案操作在不同平台可能回報不同的 `OSError` 子類別，需要查看實際錯誤，而不是只憑副檔名判斷。

---

## 單元十一｜`try`、`except`、`else` 與 `finally`

### 11-1｜捕捉特定例外

```python
text = "abc"

try:
    number = int(text)
except ValueError:
    print("請提供整數文字")
else:
    print("轉換結果：", number)
```

先執行 `try`。發生符合的例外時，跳到 `except`；沒有例外時才執行 `else`。

如果 `int(text)` 失敗，`number` 不一定已經取得值。把使用結果的程式放在 `else`，可以避免失敗後仍誤用尚未建立的變數。

### 11-2｜取得錯誤物件

```python
text = "abc"

try:
    number = int(text)
except ValueError as error:
    print(f"無法轉換 {text!r}：{error}")
```

`as error` 取得例外物件，方便補充訊息。f-string 的 `!r` 使用 `repr()` 的表示方式。

### 11-3｜分別處理不同問題

```python
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "students.json"

try:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
except FileNotFoundError:
    print(f"找不到檔案：{path}")
except UnicodeDecodeError:
    print("檔案不是可用 UTF-8 讀取的文字")
except json.JSONDecodeError as error:
    print(f"JSON 格式錯誤，第 {error.lineno} 行、第 {error.colno} 欄")
except OSError as error:
    print(f"無法讀取檔案：{error}")
else:
    print("解析成功，最外層型別：", type(data).__name__)
```

`FileNotFoundError` 是 `OSError` 的子類別，所以較具體的處理應放前面。否則先被廣泛的例外類別接住，就不會進入後面的特定分支。

不同例外需要相同處理時，也可寫成 `except (TypeError, ValueError) as error:`。

### 11-4｜`finally` 的用途

```python
try:
    number = int("abc")
except ValueError:
    print("轉換失敗")
finally:
    print("本次嘗試結束")
```

一般控制流程離開 `try` 敘述時，不論成功或發生例外，都會執行 `finally`。未處理的例外不會因此消失，而是在清理後繼續往外傳遞。

`finally` 常用來釋放資源；檔案開關通常直接使用 `with` 更清楚。程式被作業系統強制終止或電腦斷電時，不能保證清理一定完成。

不要在 `finally` 隨意 `return`，因為可能覆蓋原本的回傳或遮住例外。

### 11-5｜不要把錯誤藏起來

以下是應避免的處理方式：

```text
try:
    讀取並處理資料
except Exception:
    pass
```

它會讓失敗看起來像沒有發生。應先判斷程式能否合理處理這個問題；能處理就提供明確回應，不能處理則保留錯誤，讓呼叫端得知失敗。

`except:` 沒有指定類別時，還可能接住使用者中斷等訊號，更不應當作通用修補方法。

### 11-6｜反覆要求有效輸入

```python
while True:
    text = input("請輸入 0～100 的分數，或 q 離開：").strip()

    if text.lower() == "q":
        print("已取消")
        break

    try:
        score = float(text)
    except ValueError:
        print("請輸入數字")
        continue

    if not 0 <= score <= 100:
        print("分數必須介於 0 到 100")
        continue

    print(f"收到分數：{score:.1f}")
    break
```

先試試 `abc`、`105`、`82.5`，再重新執行測試 `q`。字串轉數值與數值範圍是兩個分開的檢查。

---

## 單元十二｜`raise` 與函式輸入驗證

### 12-1｜由函式明確表達失敗

```python
def validate_score(score):
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("分數必須是數值，不能是布林值或字串")
    if not 0 <= score <= 100:
        raise ValueError("分數必須介於 0 到 100")
    return score


for value in [82, 82.5, 105, "82", True]:
    try:
        print("有效：", validate_score(value))
    except (TypeError, ValueError) as error:
        print(f"無效：{value!r}，{error}")
```

`raise` 主動提出例外，不會自動顯示友善介面；訊息如何呈現，由呼叫端決定。

`isinstance()` 判斷物件是否屬於某種型別或其子類別。Python 的 `bool` 是 `int` 的子類別，因此這裡先排除布林值，避免把 `True` 當成 `1` 分。

### 12-2｜為什麼不全部自動轉型？

互動輸入本來就是文字，將 `input()` 的結果轉成數值很合理。

但 JSON 已經區分數字 `82` 與字串 `"82"`。當資料規格要求數值時，默默將錯誤型別轉換，可能讓上游資料問題不容易被發現。

先決定接受的資料格式，再進行明確轉換或拒絕，不要在各個函式中任意猜測。

### 12-3｜解析成功不代表符合資料規格

下面都是可以解析的 JSON：

```json
{"name": "小安"}
```

```json
{"name": "小安", "score": "82"}
```

```json
null
```

但它們都不符合「多筆學生資料，每筆有姓名與數值分數」的要求。

驗證時需要逐層確認：最外層型別、是否為空、每筆型別、必要欄位、欄位型別，以及合理範圍。

### 12-4｜保留原始錯誤的原因

```python
def parse_score(text):
    try:
        score = int(text)
    except ValueError as error:
        raise ValueError(f"分數欄位不是整數：{text!r}") from error
    return score


try:
    parse_score("abc")
except ValueError as error:
    print(error)
    print("原始原因型別：", type(error.__cause__).__name__)
```

`raise ... from error` 補上更有意義的情境，同時保留原始原因。若只想原樣向外重新提出正在處理的例外，可在 `except` 中直接寫 `raise`。

### 小練習

將 `scores.txt` 的讀取程式改成：任何一行無法轉成整數或超出範圍時，顯示錯誤行號並停止，不產生部分結果。空白行仍可略過。

---

## 單元十三｜列出檔案與檢查副檔名

### 13-1｜走訪資料夾

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
input_dir = BASE_DIR / "lesson03_data" / "input"

for path in sorted(input_dir.iterdir(), key=lambda item: item.name):
    if path.is_file():
        print(path.name, path.stat().st_size, "bytes")
```

`.iterdir()` 列出直接位於資料夾中的項目，包含檔案與子資料夾，順序不保證固定，因此上例自行排序。

`.stat().st_size` 是檔案位元組數，不是文字字數。

### 13-2｜`glob()` 與 `rglob()`

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
input_dir = BASE_DIR / "lesson03_data" / "input"

for path in sorted(input_dir.glob("*.txt")):
    if path.is_file():
        print(path.name)
```

`glob("*.txt")` 找出符合模式的路徑；`rglob("*.txt")` 會繼續搜尋子資料夾。

不同平台的檔名大小寫規則可能不同。若要明確接受 `.TXT` 與 `.txt`，可以逐一檢查 `path.suffix.lower()`。

### 13-3｜副檔名是分類線索，不是內容證明

```python
from pathlib import Path


def inspect_file(filename):
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"找不到檔案：{path}")
    if not path.is_file():
        raise ValueError(f"路徑不是一般檔案：{path}")

    suffix = path.suffix.lower()
    if suffix == ".txt":
        kind = "text"
    elif suffix == ".json":
        kind = "json"
    else:
        raise ValueError(f"不支援的副檔名：{suffix or '沒有副檔名'}")

    return {"name": path.name, "suffix": suffix, "kind": kind}


BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "lesson03_data" / "input" / "students.json"
print(inspect_file(path))
```

將一般文字改名成 `.json`，不會讓內容變成 JSON。這個函式只做路徑與副檔名檢查，分類後仍需真正解析內容。

它也不是完整的上傳檔案安全機制；檔案大小、存取範圍、內容驗證等需要另外設計。不要把通過副檔名檢查理解成可以安全處理任意來源的檔案。

---

## 綜合實作｜從 JSON 產生成績報告

### 一、處理流程

```text
讀取 students.json
        ↓
解析 JSON
        ↓
驗證每一筆資料
        ↓
計算摘要
        ↓
建立新的 report.json
        ↓
顯示輸出位置
```

程式採用以下資料規則：最外層是非空串列，每筆是字典，姓名是非空字串，分數是 `0` 到 `100` 的數值，不接受布林值或數字字串。

任何一筆無效就停止，不輸出只有部分資料的報告。原始輸入不改動；輸出檔已存在時拒絕覆寫。

### 二、完整程式

建立 **`lesson03_report.py`**，與 `prepare_lesson03.py` 放在同一資料夾：

```python
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "lesson03_data" / "input" / "students.json"
OUTPUT_PATH = BASE_DIR / "lesson03_data" / "output" / "report.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_students(data):
    if not isinstance(data, list):
        raise ValueError("最外層必須是學生資料串列")
    if not data:
        raise ValueError("學生資料不可為空")

    validated = []
    for number, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {number} 筆必須是字典")

        name = item.get("name")
        score = item.get("score")

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"第 {number} 筆缺少有效姓名")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"第 {number} 筆分數必須是數值")
        if not 0 <= score <= 100:
            raise ValueError(f"第 {number} 筆分數必須介於 0 到 100")

        validated.append({"name": name.strip(), "score": score})

    return validated


def make_report(students):
    scores = [student["score"] for student in students]
    passed_names = [
        student["name"]
        for student in students
        if student["score"] >= 60
    ]

    return {
        "count": len(students),
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "passed_count": len(passed_names),
        "passed_names": passed_names,
    }


def save_report(path, report):
    text = json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
        allow_nan=False,
    ) + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as file:
        file.write(text)


def main():
    try:
        data = load_json(INPUT_PATH)
        students = validate_students(data)
        report = make_report(students)
        save_report(OUTPUT_PATH, report)
    except FileNotFoundError as error:
        print(f"找不到需要的路徑：{error.filename}")
        return 1
    except FileExistsError:
        print("輸出檔已存在，請修改 OUTPUT_PATH 使用新的檔名")
        return 1
    except UnicodeDecodeError:
        print("輸入檔必須使用 UTF-8 編碼")
        return 1
    except json.JSONDecodeError as error:
        print(f"JSON 格式錯誤：第 {error.lineno} 行、第 {error.colno} 欄")
        return 1
    except ValueError as error:
        print(f"資料錯誤：{error}")
        return 1
    except OSError as error:
        print(f"檔案操作失敗：{error}")
        return 1

    print(f"人數：{report['count']}")
    print(f"平均：{report['average']:.2f}")
    print(f"及格人數：{report['passed_count']}")
    print(f"已建立：{OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 三、執行與結果

先執行 `python prepare_lesson03.py`，再執行 `python lesson03_report.py`。

使用未修改的練習素材時，終端機會顯示人數 `4`、平均 `75.00`、及格人數 `3`，以及實際輸出位置。

`report.json` 的內容應為：

```json
{
  "count": 4,
  "average": 75.0,
  "highest": 91,
  "lowest": 58,
  "passed_count": 3,
  "passed_names": [
    "小安",
    "小晴",
    "小庭"
  ]
}
```

`sys.exit(main())` 將 `main()` 的回傳值作為程式結束狀態。`0` 表示成功，這個程式用 `1` 表示失敗，讓其他工具也能區分是否完成。

### 四、函式的責任

`load_json()` 只負責讀取與解析，不猜測資料用途。

`validate_students()` 檢查資料，並建立清理過姓名的新串列，不直接修改原本的字典。

`make_report()` 接收已驗證的非空資料並統計；不能跳過驗證就任意傳入空資料。

`save_report()` 先把資料轉成 JSON 文字，再建立輸出檔，避免序列化失敗時已先建立一個空檔。檔案寫入期間仍可能因 I/O 問題失敗，這個練習沒有實作完整的原子寫入與復原機制。

### 五、測試不同輸入

將需要變更的測試資料另存為 `students_practice.json`，並修改程式的 `INPUT_PATH` 指向它。需要保留不同報告時，同時換一個新的 `OUTPUT_PATH`，例如 `report_practice.json`。

| 測試情況 | 預期行為 |
| --- | --- |
| 原始四筆資料 | 平均 `75.0`，及格 `3` 人 |
| 分數恰好為 `60` | 計入及格 |
| 分數為 `0` 或 `100` | 合法邊界值 |
| 姓名前後有空白 | 報告使用去除前後空白的姓名 |
| 缺少 `name` 或 `score` | 回報資料錯誤 |
| 姓名為空字串或只有空白 | 回報資料錯誤 |
| 分數為 `"82"`、`true` 或 `null` | 回報資料錯誤，不自動當成數值 |
| 分數為 `-1` 或 `101` | 回報資料錯誤 |
| 最外層是 `{}`、`null` 或空串列 | 回報資料錯誤 |
| JSON 少了逗號或括號 | 顯示 JSON 錯誤位置 |
| 輸出檔已存在 | 保留舊檔，回報失敗 |

Python 的 JSON 解碼器預設還可能接受非標準的 `NaN` 與無限大表示。本例的數值範圍檢查也會拒絕這些分數，輸出端另以 `allow_nan=False` 限制結果格式。

### 六、修改練習

1. 增加未及格人數與姓名。
2. 讓報告保存依分數排序的姓名與分數。
3. 將及格門檻改成參數，並驗證門檻範圍。
4. 在每筆資料中增加 `student_id`，檢查是否有重複編號。
5. 將讀取、驗證與統計函式移至獨立模組，主程式只負責串接與顯示。

---

## 常見問題與排查順序

### 找不到明明存在的檔案

先顯示 `Path.cwd()` 與目標路徑的 `.resolve()`，確認程式實際查找的位置。再檢查檔名、大小寫、副檔名，以及檔案是否被存成 `message.txt.txt`。

### 中文讀取失敗

檢查檔案實際編碼是否為 UTF-8。不要為了讓錯誤消失就加上忽略解碼錯誤的設定，否則可能悄悄遺失內容。

### JSON 可以打開，但程式說格式錯誤

文字編輯器能顯示內容，不代表內容符合 JSON 語法。檢查雙引號、逗號、括號與 `true / false / null` 的大小寫。

### JSON 解析成功，但取欄位失敗

解析只保證得到資料，不保證最外層型別與欄位符合需求。先查看 `type(data).__name__`，再驗證資料結構。

### 重跑後檔案內容消失或重複

檢查開檔模式。`"w"` 覆寫，`"a"` 附加，`"x"` 拒絕同名檔。三種行為不同，不應只為了避免錯誤訊息就任意更換。

### 顯示成功，但其實沒有結果

檢查是否用過廣泛的 `except` 吞掉錯誤，以及成功訊息是否在真正寫入完成之後才顯示。

---

## 章末自我檢查

1. 相對路徑是相對於哪個位置？它一定是 `.py` 所在位置嗎？
2. `Path(...)`、`.resolve()`、`.mkdir()` 各自會做什麼？
3. `.name`、`.stem`、`.suffix` 與 `.parent` 分別代表什麼？
4. 為什麼中文文字的字元數不等於 UTF-8 位元組數？
5. 離開 `with` 區塊後，哪些資料還可以使用？
6. `"r"`、`"w"`、`"a"`、`"x"` 的差別是什麼？
7. 文字模式與二進位模式分別處理哪種 Python 型別？
8. `json.dumps()` 與 `json.dump()` 的輸出對象有何不同？
9. 為什麼 `str(dict)` 不能取代 JSON 序列化？
10. JSON 解析成功後，還需要做哪些驗證？
11. 語法錯誤、執行時例外與邏輯錯誤有何差異？
12. `else` 與 `finally` 分別在什麼情況執行？
13. 為什麼較具體的例外類別應放在前面？
14. 函式何時應該 `raise`，何時由呼叫端顯示提示？
15. 為什麼副檔名不能證明檔案內容？
16. 如何確認程式沒有覆寫輸入檔，也沒有把失敗當成成功？

---

## 與後續專題的連結

圖片與樂譜資料同樣需要可靠的路徑、清楚的輸入輸出位置，以及可以追查的錯誤訊息。

後續讀取圖片時，可以沿用 `Path` 與檔案檢查；保存辨識結果時，可以使用 JSON；整合多個功能時，則讓函式回傳資料，並將無法完成的情況明確交給呼叫端處理。

## 延伸閱讀

- [Python 3.11：輸入與輸出](https://docs.python.org/3.11/tutorial/inputoutput.html)
- [Python 3.11：pathlib](https://docs.python.org/3.11/library/pathlib.html)
- [Python 3.11：JSON](https://docs.python.org/3.11/library/json.html)
- [Python 3.11：錯誤與例外](https://docs.python.org/3.11/tutorial/errors.html)
- [Python 3.11：內建函式](https://docs.python.org/3.11/library/functions.html)
