# 第 19 章｜為什麼要拆檔案：模組、import 與正式專案架構

到第 18 章為止，學生已經真的做過每個功能。現在才適合回答：**為什麼完整專案有這麼多檔案？**

因為我們不是為了「看起來專業」而拆，而是每一組功能已經有明確責任。

## 學習目標

- 根據責任拆分程式檔案。
- 理解 package、`__init__.py` 與 import。
- 建立 `app/services/` 架構。
- 將前面已完成的函式移到正式位置。
- 理解 private helper 的 `_name` 命名慣例。

[TOC]

---

## 一、如果全部都在 main.py 會怎樣？

假設一支檔案同時有：

```text
OpenCV
XML parser
Do Re Mi
subprocess
FastAPI
HTML
測試
```

出錯時很難知道哪裡屬於哪個責任，也很難單獨測試。

我們現在已經能自然分成：

```text
converter        → 音符轉標註
musicxml         → MusicXML 讀寫
image_preprocessor → 圖片前處理
omr              → 呼叫 OMR
pipeline         → 決定流程順序
web              → HTTP / API
```

---

## 二、建立正式資料夾

```text
scoresense/
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
├── static/
├── tests/
├── main.py
└── requirements.txt
```

此時學生應該可以說出每個檔案為什麼存在。

---

## 三、package 與 __init__.py

`app/` 和 `app/services/` 放入空的：

```text
__init__.py
```

讓 Python 清楚把它們當成 package。

例如：

```python
from app.services.converter import pitch_to_label
```

---

## 四、搬移 converter

把第 9、10 章成熟的：

```text
LabelMode
PitchInfo
BASE_LABELS
pitch_to_label
```

移進：

```text
app/services/converter.py
```

---

## 五、搬移 MusicXML

把：

```text
AnnotatedNote
local_name
child
extract_pitch
annotate_musicxml
save_note_report
```

整理進：

```text
app/services/musicxml.py
```

這時因為 converter 已經是另一個模組，可以：

```python
from .converter import LabelMode, PitchInfo, pitch_to_label
```

前面的 `.` 表示同一個 package 中的相對 import。

---

## 六、`_helper()` 的底線

完整 MVP 中會看到：

```python
def _child(...):
    ...
```

前面的 `_` 是一種慣例：

> 這是模組內部輔助函式，不是主要對外 API。

它不是真正的存取權限鎖，但能幫助閱讀者分辨：

```text
主要功能
vs
內部實作細節
```

---

## 七、config.py

把共用目錄與格式放在：

```text
app/config.py
```

例如：

```python
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
WORK_DIR = DATA_DIR / "work"
OUTPUT_DIR = DATA_DIR / "outputs"
STATIC_DIR = ROOT_DIR / "static"
```

再定義：

```python
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_MUSICXML_EXTENSIONS = {".xml", ".musicxml", ".mxl"}
```

這樣不同檔案不必各自寫一份。

---

## 本章重構任務

不是重新寫功能，而是：

```text
把已經驗證的功能搬到正確位置
↓
修改 import
↓
一個一個再測
```

每搬一個模組就跑最小測試，不要全部搬完才第一次執行。

---

## 章末檢核

1. 為什麼前 18 章沒有一開始就丟這個架構？
2. converter.py 的責任是什麼？
3. pipeline.py 為什麼不應該自己實作 OpenCV 細節？
4. `_child()` 前面的底線代表什麼慣例？
5. config.py 適合放哪類資訊？
