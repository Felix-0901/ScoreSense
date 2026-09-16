# 第 5 章｜OpenCV：讀圖、座標、裁切與輸出

上一章我們用 NumPy 自己建立影像陣列。現在開始讀真正的圖片。

本章的重點不是「會呼叫 `cv2.imread()` 就算會 OpenCV」，而是每做一步都檢查資料的 `shape`、型別與結果。

## 學習目標

- 使用 OpenCV 讀取彩色與灰階圖片。
- 檢查圖片是否成功讀取。
- 理解 OpenCV 的 BGR 顏色順序。
- 使用 NumPy 切片裁切樂譜。
- 儲存處理後影像並核對輸出。

[TOC]

---

## 單元一｜第一次讀取樂譜圖片

使用：

```text
materials/score_clean.png
```

建立 `lesson05_read.py`：

```python
import cv2

image = cv2.imread("materials/score_clean.png")

if image is None:
    raise FileNotFoundError("圖片讀取失敗")

print("shape:", image.shape)
print("dtype:", image.dtype)
```

### 為什麼一定要檢查 `None`？

`cv2.imread()` 讀不到圖片時，不一定直接丟出你想像中的錯誤，而可能回傳 `None`。

如果下一行馬上寫：

```python
image.shape
```

錯誤會變成：

```text
'NoneType' object has no attribute 'shape'
```

這時真正問題其實是「前一步讀檔失敗」。

---

## 單元二｜寬、高與通道

```python
height, width, channels = image.shape

print("width:", width)
print("height:", height)
print("channels:", channels)
```

請注意 `shape` 是：

```text
(height, width, channels)
```

---

## 單元三｜裁切

例如：

```python
crop = image[40:240, 30:600]
```

意思是：

```text
y：40 到 239
x：30 到 599
```

建立：

```python
cv2.imwrite("output/crop.png", crop)
```

先建立輸出資料夾：

```python
from pathlib import Path
Path("output").mkdir(exist_ok=True)
```

### 修改練習

1. 裁左半邊。
2. 裁右半邊。
3. 裁最上方 100 像素。
4. 故意把 `x` 和 `y` 寫反，觀察結果。

---

## 單元四｜灰階讀取

```python
gray = cv2.imread("materials/score_clean.png", cv2.IMREAD_GRAYSCALE)

print(gray.shape)
print(gray.dtype)
```

灰階圖通常只有：

```text
(height, width)
```

因為每個像素只需要一個亮度值。

也可以先讀彩色再轉灰階：

```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

---

## 單元五｜為什麼專案不用依賴 `cv2.imshow()`？

`cv2.imshow()` 在有 GUI 的本機環境很好用，但伺服器或某些 headless 環境不一定能開視窗。

ScoreSense 最後是 Web 系統，因此核心流程盡量採用：

```text
讀取
↓
處理
↓
存檔
↓
由瀏覽器或檔案檢視器查看
```

這也是為什麼 MVP 使用 `opencv-python-headless`。

---

## 單元六｜支援中文路徑的讀寫方式

有些 OpenCV 版本或環境對特殊字元路徑可能出現問題。MVP 採用：

```python
import cv2
import numpy as np

raw = np.fromfile("圖片/樂譜.png", dtype=np.uint8)
image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
```

寫出則可以：

```python
ok, buf = cv2.imencode(".png", image)
if not ok:
    raise ValueError("圖片編碼失敗")
buf.tofile("輸出/結果.png")
```

現在先理解概念即可。第 8 章會正式包成 `_read_image()` 與 `_write_image()`。

---

## 綜合實作｜建立圖片檢查器

```python
from pathlib import Path
import cv2


def inspect_image(filename):
    path = Path(filename)
    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"無法讀取圖片：{path}")

    h, w = image.shape[:2]
    return {
        "name": path.name,
        "width": w,
        "height": h,
        "channels": image.shape[2],
        "dtype": str(image.dtype),
    }


print(inspect_image("materials/score_clean.png"))
```

### 思考

之後如果使用者上傳一張超級大的手機照片，我們是不是應該先知道尺寸？為什麼？

---

## 章末檢核

1. `cv2.imread()` 失敗可能回傳什麼？
2. `image.shape` 的前三個值順序是什麼？
3. `image[y1:y2, x1:x2]` 在做什麼？
4. 為什麼核心程式不一定要使用 `cv2.imshow()`？
5. BGR 與 RGB 有什麼差別？
