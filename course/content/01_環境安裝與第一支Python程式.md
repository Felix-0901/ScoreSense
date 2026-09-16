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
建立環境時明確指定 Python 3.11，避免使用到電腦上其他版本的 Python。
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

## 單元三｜一步一步建立 Python 專題環境

接下來在自己的電腦上，依序完成：安裝 Python 3.11、建立專案資料夾、建立虛擬環境，再安裝後續課程使用的套件。

本機 Python 用來建立虛擬環境；專案套件裝在 `.venv`，自己的程式則放在外面：

```text
scoresense_course/
├── .venv/       專案專用的 Python 與套件
└── hello.py     自己寫的程式
```

依照自己的作業系統，完成下面其中一組操作。

### 3-1｜Windows：安裝本機 Python

開啟 PowerShell，安裝 Python 3.11：

```powershell
winget install -e --id Python.Python.3.11 --source winget
```

完成後關閉 PowerShell，再重新開啟，確認版本：

```powershell
py -3.11 --version
```

應看到 `Python 3.11.x`。`py -3.11` 明確指定使用 3.11，不會因為電腦同時有其他版本而選錯。

### 3-2｜Windows：建立專案與虛擬環境

先在家目錄的 `projects` 下建立專案資料夾，再進入：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\projects\scoresense_course"
Set-Location "$HOME\projects\scoresense_course"
Get-Location
```

`New-Item` 建立資料夾，`Set-Location` 切換位置，`Get-Location` 顯示所在位置。接下來的指令都在 `scoresense_course` 裡執行。

建立虛擬環境：

```powershell
py -3.11 -m venv .venv
```

`-m venv` 是執行 Python 內建的虛擬環境工具，最後的 `.venv` 是環境資料夾名稱。

啟用環境：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 顯示無法執行指令碼，在目前視窗執行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

啟用後，提示字元前方通常會出現 `(.venv)`。確認版本與路徑：

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

應看到 Python 3.11，路徑結尾應為 `scoresense_course\.venv\Scripts\python.exe`。

設定目前視窗的 Python 使用 UTF-8，並更新環境內的 pip：

```powershell
$env:PYTHONUTF8 = "1"
python -m pip install --upgrade pip
```

### 3-3｜Windows：依用途安裝套件

保持虛擬環境啟用，依序執行以下指令。這些套件都會安裝到專案的 `.venv`。

**第一步：影像處理。** NumPy 負責陣列運算，OpenCV 負責讀圖與前處理。

```powershell
python -m pip install numpy==1.26.4 opencv-python-headless==4.8.1.78
```

**第二步：網頁服務。** FastAPI 建立 API，Uvicorn 啟動服務，python-multipart 處理檔案上傳。

```powershell
python -m pip install fastapi==0.128.2 "uvicorn[standard]==0.48.0" python-multipart==0.0.20
```

**第三步：辨識工具需要的影像與數學套件。**

```powershell
python -m pip install matplotlib==3.7.5 pillow==12.3.0 scipy==1.10.1 scikit-learn==1.2.0
```

**第四步：下載工具與型別依賴。** `types-tensorflow` 是型別描述套件，不是 TensorFlow 推論引擎。

```powershell
python -m pip install requests==2.34.2 types-Pillow==10.2.0.20240822 types-tensorflow==2.18.0.20260827 typing-extensions
```

**第五步：ONNX Runtime 與 oemer。** ONNX Runtime 執行模型，oemer 負責樂譜辨識流程。

```powershell
python -m pip install onnxruntime-gpu==1.17.1 oemer==0.1.8
```

本章先完成套件安裝；模型下載與 ONNX 推論驗證，等後續開始圖片辨識時再操作。

### 3-4｜macOS：安裝本機 Python

開啟「終端機」。先依 [Homebrew 官網](https://brew.sh/)完成 Homebrew 安裝及畫面上的設定步驟，再重新開啟終端機。

安裝 Python 3.11：

```bash
brew install python@3.11
```

確認版本：

```bash
"$(brew --prefix python@3.11)/bin/python3.11" --version
```

應看到 `Python 3.11.x`。`brew --prefix python@3.11` 會取得 Python 的安裝位置，不必自己猜測路徑。

### 3-5｜macOS：建立專案與虛擬環境

在家目錄的 `projects` 下建立專案資料夾，再進入：

```bash
mkdir -p ~/projects/scoresense_course
cd ~/projects/scoresense_course
pwd
```

`mkdir -p` 建立資料夾，`cd` 切換位置，`pwd` 顯示目前位置。

使用剛才安裝的 Python 建立虛擬環境：

```bash
"$(brew --prefix python@3.11)/bin/python3.11" -m venv .venv
```

啟用環境：

```bash
source .venv/bin/activate
```

確認版本與路徑：

```bash
python --version
python -c "import sys; print(sys.executable)"
```

應看到 Python 3.11，路徑結尾應為 `scoresense_course/.venv/bin/python`。

更新環境內的 pip：

```bash
python -m pip install --upgrade pip
```

### 3-6｜macOS：依用途安裝套件

保持虛擬環境啟用，依序執行以下指令。

**第一步：影像處理。**

```bash
python -m pip install numpy==1.26.4 opencv-python-headless==4.8.1.78
```

**第二步：網頁服務與檔案上傳。**

```bash
python -m pip install fastapi==0.128.2 "uvicorn[standard]==0.48.0" python-multipart==0.0.20
```

**第三步：辨識工具需要的影像與數學套件。**

```bash
python -m pip install matplotlib==3.7.5 pillow==12.3.0 scipy==1.10.1 scikit-learn==1.2.0
```

**第四步：下載工具與型別依賴。**

```bash
python -m pip install requests==2.34.2 types-Pillow==10.2.0.20240822 types-tensorflow==2.18.0.20260827 typing-extensions
```

**第五步：macOS 使用的 ONNX Runtime。**

```bash
python -m pip install onnxruntime==1.18.1
```

**第六步：oemer。**

```bash
python -m pip install --no-deps oemer==0.1.8
```

`--no-deps` 讓 oemer 使用前面已安裝好的套件，避免它自動要求 macOS 不適用的 `onnxruntime-gpu`。

macOS 的套件安裝到這裡完成。模型下載與 ONNX 推論驗證，等後續開始圖片辨識時再操作。

### 3-7｜設定 VS Code 並執行第一支程式

用 VS Code 的「開啟資料夾」開啟 `scoresense_course`，安裝 Microsoft 的 Python 擴充套件。

開啟命令選擇區：

- Windows：`Ctrl+Shift+P`。
- macOS：`Command+Shift+P`。

搜尋 `Python: Select Interpreter`，選取這個專案的 `.venv`。這樣 VS Code 才會使用剛才安裝套件的 Python。

在專案根目錄建立單元一的 `hello.py`：

```python
print("Hello, ScoreSense!")
print(3 + 5)
```

在已啟用虛擬環境的終端機執行：

```bash
python hello.py
```

應看到：

```text
Hello, ScoreSense!
8
```

### 3-8｜下次開啟專案時

Python、虛擬環境與套件只需要安裝一次。下次開啟終端機，只要進入資料夾、啟用環境，再執行程式。

Windows：

```powershell
Set-Location "$HOME\projects\scoresense_course"
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8 = "1"
python hello.py
```

macOS：

```bash
cd ~/projects/scoresense_course
source .venv/bin/activate
python hello.py
```

結束工作時可輸入 `deactivate`，離開目前終端機的虛擬環境。

### 本單元檢查

- 電腦已安裝 Python 3.11。
- 已建立 `scoresense_course`，並在裡面建立 `.venv`。
- 終端機與 VS Code 都使用專案的 `.venv`。
- 已依序完成自己作業系統的套件安裝步驟。
- 可以執行 `hello.py`，看到預期輸出。

---

## 單元四｜pip 與 import 不是同一件事

後面會看到：

```python
import cv2
```

但如果電腦根本沒有安裝 OpenCV，`import cv2` 就會失敗。

關係是：

```text
python -m pip install opencv-python-headless
        ↓
套件被安裝進虛擬環境
        ↓
import cv2
        ↓
程式開始使用它
```

單元三已經用 `python -m pip install` 安裝套件，這裡不用重裝。`pip` 負責把套件裝到環境裡，`import` 則是讓目前的程式載入它。

例如安裝時使用 `opencv-python-headless`，程式內卻寫 `import cv2`，因為安裝名稱與匯入名稱不一定相同。

若套件明明裝過卻無法匯入，先用單元五的方法確認執行程式的 Python 是否來自同一個 `.venv`。

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
├── check_env.py
├── hello.py
└── lesson01_notes.py
```

下一章開始，我們會學習 ScoreSense 後面非常常用的 `list`、`dict`、函式與模組。
