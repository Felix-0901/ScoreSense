# 第 20 章｜Pipeline、工作目錄與輸出管理

功能拆成模組後，還需要一個地方決定「先做什麼、再做什麼」。這就是 Pipeline。

現在才介紹 Pipeline，因為學生已經親手做過每一步，知道它不是神秘框架，只是流程協調者。

## 學習目標

- 理解 Pipeline 與 service 的責任差異。
- 根據副檔名選擇圖片路徑或 MusicXML 路徑。
- 使用 job id 隔離不同工作。
- 管理 `uploads / work / outputs`。
- 建立 `PipelineResult`。

[TOC]

---

## 一、Pipeline 不做底層工作

錯誤想法：

```text
pipeline.py 裡重新寫灰階、threshold、XML parser
```

正確方向：

```text
pipeline.py
↓ 呼叫
preprocess_score()
run_oemer()
annotate_musicxml()
```

Pipeline 負責順序與資料傳遞。

---

## 二、為什麼要 job id？

如果兩次處理都寫：

```text
output/result.musicxml
```

第二次就會蓋掉第一次。

建立：

```python
import uuid

job_id = uuid.uuid4().hex[:12]
print(job_id)
```

每次可能得到：

```text
8f3c9c26c2a1
```

目錄：

```text
data/
├── work/
│   └── 8f3c9c26c2a1/
└── outputs/
    └── 8f3c9c26c2a1/
```

---

## 三、兩種輸入走兩條路

### MusicXML

```text
MusicXML
↓
直接 annotate
```

### 圖片

```text
圖片
↓
可選 preprocess
↓
OMR
↓
MusicXML
↓
annotate
```

程式：

```python
suffix = input_path.suffix.lower()

if suffix in ALLOWED_MUSICXML_EXTENSIONS:
    ...
elif suffix in ALLOWED_IMAGE_EXTENSIONS:
    ...
else:
    raise ValueError("不支援格式")
```

---

## 四、PipelineResult

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineResult:
    job_id: str
    output_dir: Path
    annotated_musicxml: Path
    note_report: Path
    notes: list
    source_musicxml: Path
    preprocessed_image: Path | None = None
    binary_preview: Path | None = None
    omr_log: Path | None = None
    omr_backend: str | None = None
```

為什麼保存這麼多路徑？

因為 Web API 後面需要告訴使用者：

```text
你的 MusicXML 在哪
你的預覽在哪
你的 log 在哪
```

---

## 五、process_file 的流程

偽程式：

```python
def process_file(input_path, mode, preprocess=True):
    建立 job_id
    建立 work_dir / output_dir

    if 是 MusicXML:
        複製到 work_dir
    elif 是圖片:
        if preprocess:
            做前處理
        執行 OMR
    else:
        報錯

    將 source_musicxml 自動標註
    儲存 notes.json

    return PipelineResult(...)
```

學生先寫偽程式，再看實作。

---

## 六、為什麼要分 work 與 outputs？

`work/`：中間過程。

```text
preprocessed.png
binary_preview.png
oemer.log
OMR 原始輸出
```

`outputs/`：使用者真正想拿走的結果。

```text
annotated_solfege.musicxml
notes.json
```

這會讓專案資料比較乾淨。

---

## 綜合實作

完成 `app/services/pipeline.py` 後，建立簡單測試：

```python
from app.services.pipeline import process_file

result = process_file(
    "materials/twinkle.musicxml",
    "zhuyin",
)

print(result.job_id)
print(result.annotated_musicxml)
print(len(result.notes))
```

先測 MusicXML 成功，再測圖片。

---

## 章末檢核

1. Pipeline 和 converter 的責任差異？
2. job id 解決什麼？
3. 為什麼 MusicXML 輸入不需要 OMR？
4. work 與 outputs 為什麼分開？
5. PipelineResult 為什麼比只回傳一個路徑更有用？
