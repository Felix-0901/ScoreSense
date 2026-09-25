# 第 4 章｜NumPy 與數位影像

一張圖片放大後，可以看見許多小格子。這些格子叫作「像素」。程式讀入圖片後，會用陣列保存每個像素的數值。

本章先把根目錄的圖片顯示出來，再觀察陣列、座標、色彩通道與數值運算。每次改完都看圖片，確認數字和畫面的關係。

## 學習目標

- 讀取並用 OpenCV 視窗顯示圖片。
- 看懂陣列的形狀、資料型別、座標與切片。
- 修改像素、保留原圖，並安全地調整亮度。
- 使用遮罩、統計與拼接比較影像。

[TOC]

---

## 開始之前｜圖片與執行位置

本章使用 **Python 3.11**。將一張真正的 JPEG 測試圖片放在專案根目錄，範例統一稱為 `test.jpg`。若使用 PNG，例如 `test.png`，請改程式中的檔名；不必把 PNG 的副檔名硬改成 JPG。選擇至少 32 × 32 像素的圖片，方便後面裁切與鄰域運算。

```text
ScoreSense/
├── test.jpg
├── lesson04.py
├── course/
└── …
```

用 VS Code 開啟專案根目錄，將每段完整範例依次貼入自己的 `lesson04.py`，儲存後在根目錄的終端機執行 `python lesson04.py`。各範例都從頭讀圖或建立小陣列，不需要先建立工具模組，也不依賴上一段執行後留下的變數。

`"test.jpg"` 是相對於「目前工作目錄」的路徑，不是保證相對於 `.py` 的位置。不要把練習程式命名成 `cv2.py` 或 `numpy.py`，以免遮住套件名稱。

### 視窗需要有 GUI 的 OpenCV

`opencv-python-headless` 不提供 `cv2.imshow()` 所需的視窗功能；`opencv-python` 提供桌面視窗。兩者都匯入為 `cv2`，不能在同一個環境混裝。[OpenCV 套件說明](https://pypi.org/project/opencv-python/4.8.1.78/)

若目前的環境已能開 OpenCV 視窗，直接進入單元一。若沿用的是 headless 環境，可另外建立只供影像練習的 `.venv-cv`，保留原專案 `.venv` 與 OMR 套件不動。

Windows，在專案根目錄執行：

```powershell
py -3.11 -m venv .venv-cv
.\.venv-cv\Scripts\python.exe -m pip install numpy==1.26.4 opencv-python==4.8.1.78 matplotlib==3.7.5
```

macOS 或已有 Python 3.11 的 Linux：

```bash
python3.11 -m venv .venv-cv
.venv-cv/bin/python -m pip install numpy==1.26.4 opencv-python==4.8.1.78 matplotlib==3.7.5
```

這只安裝影像練習需要的套件，不是重建整個辨識系統。VS Code 的 `Python: Select Interpreter` 選擇 `.venv-cv`，再開啟新的終端機。執行 `python -c "import sys; print(sys.executable)"`，確認指向 `.venv-cv`；也可直接用上面的 Python 執行檔路徑執行 `lesson04.py`。

桌面套件仍需要可用的桌面顯示環境。純 SSH、沒有顯示伺服器的容器或部分遠端 Notebook 不能直接跳出本機視窗。Linux 還可能需要作業系統的 GUI 相依元件；請在有桌面的電腦執行本章。

後續執行 ScoreSense／OMR 時，切回原本專案環境；不要在 `.venv-cv` 安裝整份 OMR requirements 而又混入 headless OpenCV。

---

## 單元一｜讀取與顯示一張圖片

先完成最小流程：讀取 → 確認成功 → 顯示 → 等待按鍵 → 關閉視窗。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")


cv2.imshow("Original", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 第一次出現的程式碼

| 寫法 | 意義 |
| --- | --- |
| `import cv2` | 載入 OpenCV 的 Python 介面 |
| `cv2.imread("test.jpg")` | 讀取並解碼圖片，預設取得三通道 BGR 陣列 |
| `image = ...` | 將回傳的影像陣列交給名稱 `image` |
| `image is None` | 判斷是否沒有取得圖片，不是判斷圖片是否全黑 |
| `raise FileNotFoundError(...)` | 在讀取失敗時停止並顯示提示；失敗原因也可能是檔案損壞或不支援 |
| `cv2.imshow("Original", image)` | 用名為 Original 的視窗顯示陣列，不回傳處理後圖片 |
| `cv2.waitKey(0)` | 處理視窗事件並等待按鍵；`0` 表示沒有逾時限制 |
| `cv2.destroyAllWindows()` | 關閉目前程式建立的 OpenCV 視窗 |

請點選圖片視窗，再按任意鍵。程式會繼續到關閉視窗這一行。只關閉視窗的叉叉，在部分環境不一定會結束 `waitKey(0)`。

不要寫 `image = cv2.imshow(...)`：那會用它的回傳值 `None` 蓋掉影像變數。終端機的 `print(image)` 顯示數字；`imshow` 顯示那些數字所代表的圖片。

---

## 單元二｜圖片太大時調整視窗

先調整「視窗」，不必立刻改變圖片像素。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original", 900, 600)

cv2.imshow("Original", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 新寫法 | 說明 |
| --- | --- |
| `namedWindow()` | 先建立指定名稱的視窗 |
| `WINDOW_NORMAL` | 允許調整視窗大小 |
| `resizeWindow("Original", 900, 600)` | 將視窗設為指定寬、高；不修改 `image` 的陣列尺寸 |
| `waitKey(1000)` | 等待按鍵或約 1000 毫秒；實際延遲受系統影響 |

後面範例採簡短的 `imshow()`。圖片超過螢幕時，可在對應 `imshow()` 前加入同名 `namedWindow()` 與 `resizeWindow()`；有幾張結果，就分別設定它們的視窗。

**練習：**先改視窗大小，再印出 `image.shape`。陣列尺寸有跟著改變嗎？

---

## 單元三｜NumPy 陣列與圖片資訊

NumPy 的陣列名稱是 `ndarray`。它可以用多個維度保存數值；OpenCV 讀到的圖片就是這種資料。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

print(type(image))
print("shape：", image.shape)
print("ndim：", image.ndim)
print("dtype：", image.dtype)
print("size：", image.size)
print("nbytes：", image.nbytes)
height, width = image.shape[:2]
print("像素數：", height * width)

cv2.imshow("Original", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 屬性或寫法 | 意義 |
| --- | --- |
| `shape` | 各維度長度；一般彩圖是 `(高度, 寬度, 通道數)` |
| `ndim` | 維度數；灰階通常為 2，彩圖通常為 3 |
| `dtype` | 每個元素的數值型別；本章使用 `uint8` |
| `size` | 陣列元素數，彩圖包含所有通道 |
| `nbytes` | 陣列資料所占的位元組數，不是 JPEG／PNG 檔案大小 |
| `shape[:2]` | 取前兩個維度，再分別交給 `height` 與 `width` |

例如 `(600, 800, 3)` 有 `600 × 800 = 480000` 個像素，但有 `1440000` 個通道元素。`uint8` 的 `u` 表示無號，8 表示 8 位元，可以保存整數 `0～255`。不是所有影像格式都只有這個範圍。

---

## 單元四｜灰階圖與色彩通道

灰階圖每個像素保存一個亮暗值：`0` 黑、`255` 白。BGR 彩圖則依序保存藍、綠、紅三個通道，不是 RGB。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("彩圖形狀：", image.shape)
print("灰階形狀：", gray.shape)
print("左上角 BGR：", image[0, 0])
print("左上角灰階：", gray[0, 0])

cv2.imshow("Original", image)
cv2.imshow("Gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 新寫法 | 說明 |
| --- | --- |
| `cv2.cvtColor(image, 轉換代碼)` | 依指定規則回傳色彩轉換後的新陣列 |
| `COLOR_BGR2GRAY` | 將 BGR 三通道換成單通道灰階 |
| `image[0, 0]` | 取第 0 列、第 0 欄的像素 |

常見換算近似為 `0.114B + 0.587G + 0.299R`，不是三通道直接平均。兩個不同顏色可能變成相近灰階；灰階化會捨棄色彩差異。

| BGR 值 | 顏色 |
| --- | --- |
| `(0, 0, 0)` | 黑 |
| `(255, 255, 255)` | 白 |
| `(255, 0, 0)` | 藍 |
| `(0, 255, 0)` | 綠 |
| `(0, 0, 255)` | 紅 |

---

## 單元五｜座標、切片與修改像素

左上角是原點，x 向右、y 向下。幾何座標通常寫 `(x, y)`，陣列則是 `[y, x]`。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

height, width = image.shape[:2]
x = width // 2
y = height // 2
print("中央像素：", image[y, x])

marked = image.copy()
marked[height // 4:height // 2, width // 4:width // 2] = (0, 0, 255)

cv2.imshow("Original", image)
cv2.imshow("Changed pixels", marked)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`//` 是整數除法。`.copy()` 建立獨立陣列，避免修改結果時連原圖一起改。

切片 `a:b` 包含 a、不包含 b。上例把指定區域的所有像素設成紅色，不是畫透明色塊。彩圖中的 `image[y, x, 0]` 才是該像素的藍通道值。

**練習：**改成右下角四分之一區域。先畫出範圍，再改兩組切片，不要只交換數字試運氣。

---

## 單元六｜裁切與 view

裁切選出矩形區域，不會自動辨識物體。以下取圖片中央一半寬、一半高，適用於至少 4 × 4 的測試圖。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

height, width = image.shape[:2]
y1, y2 = height // 4, 3 * height // 4
x1, x2 = width // 4, 3 * width // 4
crop = image[y1:y2, x1:x2].copy()
print("原圖：", image.shape)
print("裁切：", crop.shape)

cv2.imshow("Original", image)
cv2.imshow("Crop", crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

基本切片通常是共用資料的 view；`crop = image[y1:y2, x1:x2]` 後修改 `crop`，可能影響 `image`。加上 `.copy()` 才能獨立修改。

| 寫法 | 結果 |
| --- | --- |
| `b = a` | 兩個名稱指向同一個陣列 |
| `b = a[:2, :2]` | 基本切片，通常共用原資料 |
| `b = a[:2, :2].copy()` | 區域的獨立複本 |

切片超過邊界不一定報錯，也可能得到較小區域或空陣列。空陣列不能正常交給 `imshow()`。

**練習：**把副本全部設成白色，觀察原圖是否保持不變。

---

## 單元七｜自行建立陣列

照片適合觀察真實內容，小陣列則適合手算。`import numpy as np` 將 NumPy 簡稱為 `np`。

### 完整範例

```python
import cv2
import numpy as np

numbers = np.array([[0, 128], [200, 255]], dtype=np.uint8)
black = np.zeros((200, 300), dtype=np.uint8)
white = np.full((200, 300), 255, dtype=np.uint8)
canvas = np.full((200, 300, 3), 255, dtype=np.uint8)
canvas[50:150, 100:200] = (0, 0, 255)
print(numbers)

cv2.imshow("Black", black)
cv2.imshow("White", white)
cv2.imshow("Red block", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 建立方式 | 用途 |
| --- | --- |
| `np.array(資料, dtype=...)` | 將串列等資料建立成陣列 |
| `np.zeros((h, w), dtype=np.uint8)` | 全零，灰階黑色畫布 |
| `np.ones((h, w), dtype=np.uint8)` | 全一；灰階 1 接近黑色，不是白色 |
| `np.full((h, w), 255, dtype=np.uint8)` | 全部填入指定值 |
| `np.zeros_like(image)` | 使用另一陣列的形狀與型別建立全零陣列 |

彩色畫布多一個長度 3 的通道維度。把區域指定為三個值時，NumPy 會將它套到區域中每一個像素，這是一種「廣播」。

---

## 單元八｜數列、形狀與廣播

`arange()` 依步長建立數列；`linspace()` 依個數建立等距數列；`reshape()` 改變排列形狀，不是縮放照片。

### 完整範例

```python
import cv2
import numpy as np

numbers = np.arange(12)
print(numbers.reshape(3, 4))
levels = np.linspace(0, 255, 300).astype(np.uint8)
canvas = np.zeros((160, 300), dtype=np.uint8)
canvas[:] = levels

cv2.imshow("Gradient", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`np.arange(12)` 產生 `0～11`。12 個元素可以排成 `3 × 4`，不能直接排成 `3 × 5`。

`np.linspace(0, 255, 300)` 取得 300 個等距數值，預設包含兩端；`.astype(np.uint8)` 轉成可顯示的 8 位元整數。`canvas[:] = levels` 將同一列亮度廣播到每一列。

**觀察：**左邊黑、右邊白。左右變化來自數值，沒有繪製任何幾何圖形。

---

## 單元九｜亮度運算與溢位

NumPy 的 `uint8` 陣列加法可能回繞，例如 `250 + 20` 超過 255。先轉成較寬的型別再計算，最後限制範圍。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
work = gray.astype("int16") + 40
bright = work.clip(0, 255).astype("uint8")
print("原平均：", gray.mean())
print("加亮後平均：", bright.mean())

cv2.imshow("Gray", gray)
cv2.imshow("Brighter", bright)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 新寫法 | 意義 |
| --- | --- |
| `astype("int16")` | 轉成可保存負數及較大整數的資料 |
| `+ 40` | 每個元素加 40，不用自行寫雙層迴圈 |
| `clip(0, 255)` | 小於 0 設成 0，大於 255 設成 255 |
| `astype("uint8")` | 回到這個範例顯示所使用的型別 |
| `mean()` | 所有元素的算術平均 |

若先用 `uint8` 加到回繞，之後才 `clip()`，已經無法還原。加亮也可能讓亮部細節全變成 255，不能保證圖片更適合辨識。

---

## 單元十｜遮罩、統計與浮點表示

遮罩表示哪些位置符合條件，不代表已經知道物體種類。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
import numpy as np

mask = gray < 100
selected = np.full_like(gray, 255)
selected[mask] = gray[mask]
normalized = gray.astype(np.float32) / 255.0
print("最小、最大：", gray.min(), gray.max())
print("小於 100 的像素數：", np.count_nonzero(mask))
print("比例：", mask.mean())

cv2.imshow("Gray", gray)
cv2.imshow("Selected", selected)
cv2.imshow("Float 0 to 1", normalized)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`gray < 100` 回傳同形狀的布林陣列。`selected[mask]` 選出其中為 `True` 的位置，`np.count_nonzero()` 計算非零數量；布林值平均等於 `True` 的比例。

`float32` 浮點影像在 `imshow()` 中通常以 `0～1` 對應黑白。直接將 `0～255` 轉成浮點卻不縮放，可能看起來大片過白。布林遮罩也不要直接拿去當一般 8 位元圖片；需要時用 `mask.astype(np.uint8) * 255`。

`gray.mean(axis=0)` 每欄得到一個平均；`axis=1` 每列得到一個平均。`axis` 是被縮減的維度。

**練習：**改成 `(gray >= 80) & (gray <= 160)`。`&` 是逐元素結合條件，每個比較要加括號；不要用一般 `and` 判斷整張陣列。

---

## 綜合實作｜原圖、灰階與亮度比較

### 先想清楚

目標是比較同一張圖，不是改寫原檔。先讀彩圖，轉成灰階，取中央區域，再從同一區域產生較亮與較暗的版本。

`np.hstack()` 將陣列左右拼接，要求高度、通道與型別相容；`np.vstack()` 上下拼接，要求寬度等其他維度相容。

### 完整程式：`lesson04_compare.py`

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
import numpy as np

height, width = gray.shape
crop = gray[height // 4:3 * height // 4, width // 4:3 * width // 4].copy()
bright = (crop.astype(np.int16) + 40).clip(0, 255).astype(np.uint8)
dark = (crop.astype(np.int16) - 40).clip(0, 255).astype(np.uint8)
comparison = np.hstack([dark, crop, bright])
print("中央區域：", crop.shape)
print("左暗、中原、右亮的平均：", dark.mean(), crop.mean(), bright.mean())

cv2.imshow("Original", image)
cv2.imshow("Dark - Original crop - Bright", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 觀察與修改

比較亮暗是否改變、區域形狀是否保持、白色或黑色是否失去細節。改成上半部 ROI，再將亮度差改成 20 與 80，分次觀察。

本程式只修改記憶體中的陣列，沒有將任何結果覆寫到 `test.jpg`。

### 自我檢查

1. 為什麼 `shape` 是高在前，座標卻常說 x 在前？
2. `size` 為什麼不一定等於像素數？
3. `copy()` 和直接賦值有什麼不同？
4. 為什麼先轉型再加減，不能算完才補救？
5. 調整視窗大小、裁切、調亮，各自改變的是什麼？

## 延伸閱讀

- [NumPy 1.26 入門](https://numpy.org/doc/1.26/user/absolute_beginners.html)
- [OpenCV：HighGUI 視窗介面](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html)
