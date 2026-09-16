# 第 17 章｜用 Python 呼叫 oemer：subprocess、timeout 與日誌

上一章還需要手動在終端機輸入 `oemer ...`。現在讓 Python 自動做這件事。

這是「整合第三方工具」的重要能力。

## 學習目標

- 理解 CLI 工具與 Python 套件 import 的差別。
- 使用 `shutil.which()` 找外部命令。
- 使用 `subprocess.run()` 執行外部程式。
- 保存 stdout、stderr、return code。
- 加入 timeout、retry 與 log。

[TOC]

---

## 單元一｜不是所有第三方工具都一定用 import

OpenCV：

```python
import cv2
```

oemer 在這個 MVP 採用另一種整合方式：

```text
Python
↓
subprocess
↓
oemer 命令列程式
↓
MusicXML 檔案
```

這種方式的好處是責任清楚，也比較容易保存第三方程式的完整 log。

---

## 單元二｜確認命令存在

```python
import shutil

command = shutil.which("oemer")
print(command)
```

如果得到 `None`，代表目前環境找不到命令。

不要直接執行後才讓學生看一大串 FileNotFoundError。

---

## 單元三｜最小 subprocess

```python
import subprocess

result = subprocess.run(
    ["oemer", "materials/score_clean.png"],
    capture_output=True,
    text=True,
    check=False,
)

print("return code:", result.returncode)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
```

### return code

一般慣例：

```text
0 → 成功
非 0 → 發生問題
```

但仍然要確認輸出檔是否真的存在。

---

## 單元四｜指定工作目錄

希望所有 oemer 產生的檔案集中到：

```text
output/omr_test/
```

```python
from pathlib import Path

output_dir = Path("output/omr_test").resolve()
output_dir.mkdir(parents=True, exist_ok=True)

result = subprocess.run(
    ["oemer", str(Path("materials/score_clean.png").resolve())],
    cwd=output_dir,
    capture_output=True,
    text=True,
    check=False,
)
```

`cwd` 是外部程式執行時所在的工作資料夾。

---

## 單元五｜timeout

AI / OMR 工具有可能卡住。

```python
result = subprocess.run(
    args,
    timeout=1800,
    ...
)
```

如果超過時間：

```python
try:
    ...
except subprocess.TimeoutExpired:
    print("辨識逾時")
```

系統不能永遠卡住等待。

---

## 單元六｜保存 log

```python
log_text = f"""
Command: {' '.join(args)}
Return code: {result.returncode}
--- stdout ---
{result.stdout}
--- stderr ---
{result.stderr}
"""

Path("output/omr_test/oemer.log").write_text(
    log_text,
    encoding="utf-8",
)
```

這樣使用者說「辨識失敗」時，至少知道第三方工具當時輸出了什麼。

---

## 單元七｜fallback 再嘗試一次

MVP 設計兩次嘗試：

```python
attempts = [
    [command, str(image_path)],
    [command, "-d", str(image_path)],
]
```

第二次使用工具提供的 troubleshooting 參數，關閉其自身 deskew。

這不代表「失敗就無限重試」。

我們只針對已知、合理的替代策略做有限次重試。

---

## 單元八｜找到剛產生的 MusicXML

```python
def find_musicxml(directory):
    candidates = []

    for pattern in ("*.musicxml", "*.mxl", "*.xml"):
        candidates.extend(directory.glob(pattern))

    candidates = [
        p for p in candidates
        if p.name.lower() != "container.xml"
    ]

    if not candidates:
        return None

    return max(candidates, key=lambda p: p.stat().st_mtime)
```

「命令成功」加上「真的找到輸出檔」才算成功。

---

## 綜合實作｜run_oemer()

函式責任：

```text
輸入：image_path + output_dir
↓
找到 oemer
↓
執行
↓
必要時 fallback
↓
保存 log
↓
找 MusicXML
↓
回傳結果
```

請把它獨立放在：

```text
omr_runner.py
```

不要在這支檔案中處理 Do Re Mi。

---

## 章末檢核

1. `import` 第三方套件與 subprocess 呼叫 CLI 差在哪裡？
2. `shutil.which()` 做什麼？
3. stdout 與 stderr 為什麼都要保存？
4. timeout 解決什麼問題？
5. 為什麼 return code 0 仍要找輸出 MusicXML？
