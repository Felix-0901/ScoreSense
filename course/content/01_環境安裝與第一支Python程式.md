# 第 1 章｜環境安裝與第一支 Python 程式

這一章不會開始做樂譜辨識。先把「程式到底在哪裡執行、套件裝到哪裡、怎麼確認自己用對 Python」弄清楚。

很多專題不是壞在演算法，而是壞在「套件裝在 A 環境，程式卻用 B 環境執行」。所以環境觀念本身就是專題能力。

## 學習目標

- 分辨 VS Code、Python、終端機與 `.py` 檔案的角色。
- 使用 Python 3.11 建立虛擬環境。
- 使用 pip 安裝課程需要的基本套件。
- 執行第一支 Python 程式並確認直譯器位置。
- 將既有 C++ 的變數、判斷、迴圈概念轉成 Python 寫法。

[TOC]

---

## 單元一｜一支 Python 程式怎麼被執行？

一份 `.py` 檔案本質上只是文字。真正讀懂並執行它的是 Python 直譯器。

```text
你寫的 main.py
      ↓
Python 直譯器
      ↓
電腦執行
      ↓
終端機顯示結果
```

VS Code 是編輯器。它讓我們比較容易寫程式，但 VS Code 本身不是 Python。

### 第一個實驗

建立資料夾：

```text
scoresense_course
```

用 VS Code 開啟整個資料夾，建立：

```text
hello.py
```

輸入：

```python
print("Hello, ScoreSense!")
print(3 + 5)
```

先不要執行，口頭預測畫面會出現什麼。

執行後應看到：

```text
Hello, ScoreSense!
8
```

### 修改練習

把程式改成：

```python
name = "自己的名字"
print("Hello,", name)
print(10 * 3)
```

回答：

1. `name` 保存的是數字還是文字？
2. `=` 在這裡代表數學等號嗎？
3. 如果把引號拿掉會發生什麼？

---

## 單元二｜為什麼 ScoreSense 建議 Python 3.11？

這個專題後面會使用 OpenCV、FastAPI，並且有一個可選的 OMR 工具 `oemer`。

核心程式在較新的 Python 也可能可以執行，但為了讓 OMR 相容性比較容易控制，本教材統一以 **Python 3.11** 示範。

:::warning
不要因為電腦已經有某個 Python 就直接使用。專題最怕每個人的版本不同、套件版本也不同，最後同一份程式在不同電腦出現不同錯誤。
:::

### Windows

先安裝 Python 3.11。完成後在 PowerShell 測試：

```powershell
py -3.11 --version
```

### macOS

如果使用 Homebrew：

```bash
brew install python@3.11
python3.11 --version
```

沒有 Homebrew 也可以使用 Python 官方安裝程式。

---

## 單元三｜建立虛擬環境

在 `scoresense_course` 資料夾中執行。

### Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe --version
```

### macOS / Linux

```bash
python3.11 -m venv .venv
./.venv/bin/python --version
```

`.venv` 就像這份專題自己的工具箱。

```text
scoresense_course/
├── .venv/       ← Python 與第三方套件
└── hello.py      ← 自己寫的程式
```

不要把自己的 `.py` 檔放進 `.venv`。

---

## 單元四｜pip 與 import 不是同一件事

後面會看到：

```python
import cv2
```

但如果電腦根本沒有安裝 OpenCV，`import cv2` 就會失敗。

關係是：

```text
pip install opencv-python
        ↓
套件被安裝進虛擬環境
        ↓
import cv2
        ↓
程式開始使用它
```

先建立 `requirements.txt`：

```text
numpy==1.23.5
opencv-python-headless==4.8.1.78
fastapi==0.128.2
uvicorn[standard]==0.48.0
python-multipart==0.0.20
```

安裝：

Windows：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux：

```bash
./.venv/bin/python -m pip install -r requirements.txt
```

現在先不用理解 FastAPI。它只是後面會用到，所以先固定版本。

---

## 單元五｜確認「到底是哪個 Python」

建立 `check_env.py`：

```python
import sys

print("Python 版本：", sys.version)
print("Python 路徑：", sys.executable)
```

執行後，路徑應該指向目前專案的 `.venv`。

如果不是，代表你可能用錯環境。

---

## 單元六｜從 C++ 轉到 Python

如果學生已經學過 C++，不需要把程式設計重新學一次，只需要習慣語法差異。

### 變數

C++：

```cpp
int score = 80;
```

Python：

```python
score = 80
```

### 判斷

```python
score = 75

if score >= 60:
    print("及格")
else:
    print("不及格")
```

Python 用縮排表示區塊，不使用 `{}`。

### 迴圈

```python
for i in range(5):
    print(i)
```

結果：

```text
0
1
2
3
4
```

### 小練習｜七個音名

```python
notes = ["C", "D", "E", "F", "G", "A", "B"]

for note in notes:
    print(note)
```

這份資料之後會真的出現在 ScoreSense 裡。

---

## 綜合練習｜第一支跟專題有關的小程式

建立 `lesson01_notes.py`：

```python
notes = ["C", "D", "E", "F", "G", "A", "B"]

print("總共有", len(notes), "種基本音名")

for index, note in enumerate(notes, start=1):
    print(index, note)
```

預測輸出後再執行。

### 修改練習

1. 把順序改成 `C D E F G A B C`。
2. 只印出第 4 個音。
3. 用 `if` 判斷當音名是 `F` 時多印一句「這是 Fa」。

---

## 章末檢核

請不用看講義回答：

1. VS Code 和 Python 的工作有什麼不同？
2. `.venv` 是拿來放什麼的？
3. `pip install` 與 `import` 差在哪裡？
4. Python 為什麼很在意縮排？
5. `range(5)` 會產生哪幾個數字？

### 本章留下的積木

你現在已經有：

```text
scoresense_course/
├── .venv/
├── requirements.txt
├── check_env.py
├── hello.py
└── lesson01_notes.py
```

下一章開始，我們會學習 ScoreSense 後面非常常用的 `list`、`dict`、函式與模組。
