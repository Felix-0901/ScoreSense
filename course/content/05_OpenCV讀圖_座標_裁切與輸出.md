# 第 5 章｜OpenCV：讀圖、座標、裁切與輸出

本章繼續使用專案根目錄的 `test.jpg`，逐一學習讀圖方式、色彩通道、裁切、縮放、繪圖與輸出。每個範例都把原圖與結果放在視窗中比較。

沿用第 4 章確認可開視窗的 **Python 3.11** 學習環境。每段範例可以單獨存成根目錄的 `.py` 執行，不需要任何自訂共用檔案。圖片太大時，使用第 4 章的 `namedWindow()`／`resizeWindow()` 調整視窗。

## 學習目標

- 分辨讀圖模式、BGR／RGB、單一通道與透明通道。
- 裁出指定區域，選擇適當縮放方式。
- 翻轉、補邊、畫線、畫框與加入文字。
- 使用遮罩保留區域，將結果存成另一份檔案。

[TOC]

---

## 單元一｜比較讀圖模式

第 4 章使用 `imread()` 的預設值。本單元加上第二個參數，決定怎麼解碼。

### 完整範例

```python
import cv2

color = cv2.imread("test.jpg", cv2.IMREAD_COLOR)
gray = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
if color is None or gray is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")
print("彩圖：", color.shape)
print("灰階：", gray.shape)

cv2.imshow("Color", color)
cv2.imshow("Gray read", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 第二個參數 | 用途 |
| --- | --- |
| `cv2.IMREAD_COLOR` | 一般三通道 BGR 讀取，預設方式 |
| `cv2.IMREAD_GRAYSCALE` | 直接取得灰階陣列 |
| `cv2.IMREAD_UNCHANGED` | 盡量保留檔案的通道與位元深度，包括 PNG 的 alpha |

直接灰階解碼與彩圖經 `cvtColor()` 轉灰階，可能因解碼器計算方式而有細微差異。比較演算法時，固定同一種讀取方式。

`IMREAD_UNCHANGED` 不代表「幫你顯示得最正確」；它不自動處理所有透明背景或方向標籤問題。

---

## 單元二｜分離色彩通道

一個藍通道陣列只有一個數字，直接顯示時是亮暗圖，不是藍色照片。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

blue, green, red = cv2.split(image)
print("藍通道形狀：", blue.shape)

cv2.imshow("Original", image)
cv2.imshow("Blue values", blue)
cv2.imshow("Green values", green)
cv2.imshow("Red values", red)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.split(image)` 回傳各通道陣列。因為輸入是 BGR，變數順序也應是藍、綠、紅。

另一種等效取值方式是 `blue = image[:, :, 0]`；兩個 `:` 都表示選取全部，最後的 `0` 是通道索引。

**觀察：**圖片中紅色物體在紅通道是否比較亮？若素材只有黑白，三個通道可能幾乎相同，這不是失敗。

---

## 單元三｜合併通道與保留單一顏色

要真的看到藍色影像，需要三通道中只有 B 有值，G、R 都設成零。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

import numpy as np

blue, green, red = cv2.split(image)
zeros = np.zeros_like(blue)
blue_only = cv2.merge([blue, zeros, zeros])
restored = cv2.merge([blue, green, red])
print("合併後相同：", np.array_equal(image, restored))

cv2.imshow("Original", image)
cv2.imshow("Blue as gray", blue)
cv2.imshow("Blue only", blue_only)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 新寫法 | 說明 |
| --- | --- |
| `cv2.merge([b, g, r])` | 將同形狀、同型別通道合成彩圖 |
| `np.array_equal(a, b)` | 檢查陣列形狀與所有元素是否相同 |

**練習：**分別顯示 `green_only`、`red_only`，並解釋它們和單通道灰階視窗的差別。

---

## 單元四｜BGR 與 RGB 不要混用

`cv2.imshow()` 期待 BGR 彩圖，Matplotlib 等工具常期待 RGB。只在交給需要 RGB 的工具時轉換，不能轉完 RGB 又照樣交給 OpenCV 當 BGR。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
back_to_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

cv2.imshow("Correct BGR", image)
cv2.imshow("RGB shown as BGR - wrong", rgb)
cv2.imshow("Converted back", back_to_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

中間視窗是故意的錯誤示範，紅藍會互換。原圖若沒有明顯色彩差異，效果可能不明顯。

| 轉換代碼 | 用途 |
| --- | --- |
| `COLOR_BGR2GRAY` | 彩圖轉灰階 |
| `COLOR_GRAY2BGR` | 複製灰階至三通道，方便畫彩色標記；不能恢復原色 |
| `COLOR_BGR2RGB` | BGR 排列轉成 RGB |
| `COLOR_RGB2BGR` | RGB 排列轉回 BGR |

這些都是 `cvtColor()` 的參數，不是拿來單獨呼叫的函式。

---

## 單元五｜讀取並處理透明圖片

透明 PNG 多一個 alpha 通道：`0` 表示透明，`255` 表示不透明。`imshow()` 不是一般圖片檢視器，不能假設它會按透明度合成白底。

以下仍讀 `test.jpg`，再建立半透明效果來理解運算；使用真正透明 PNG 時，可將檔名改為 `test.png`。

### 完整範例

```python
import cv2
import numpy as np

source = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED)
if source is None:
    raise FileNotFoundError("讀不到圖片")
if source.dtype != np.uint8:
    raise ValueError("這個範例使用 8 位元圖片")

if source.ndim == 2:
    image = cv2.cvtColor(source, cv2.COLOR_GRAY2BGR)
    alpha = np.full((*source.shape, 1), 0.5, dtype=np.float32)
elif source.shape[2] == 4:
    image = source[:, :, :3]
    alpha = source[:, :, 3:4].astype(np.float32) / 255.0
else:
    image = source
    alpha = np.full((*image.shape[:2], 1), 0.5, dtype=np.float32)

on_white = image.astype(np.float32) * alpha + 255 * (1 - alpha)
on_white = np.rint(on_white).clip(0, 255).astype(np.uint8)

cv2.imshow("Color values", image)
cv2.imshow("On white", on_white)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

新寫法逐項看：`*image.shape[:2]` 把高度、寬度展開；加上最後的 `1`，使 alpha 形狀成為 `(h, w, 1)`。`3:4` 也保留這個單通道維度，以便廣播到 B、G、R。

`np.rint()` 將浮點數取到最近整數，再轉為 `uint8`。公式是「原色 × 不透明度 + 白色 × 透明度」。本例是理解通道合成，沒有涵蓋嚴格的線性色彩空間合成。

一般 JPEG 沒有透明通道，這裡用 `0.5` 示範；真正四通道 PNG 則使用原本 alpha。

---

## 單元六｜ROI 裁切

ROI 是感興趣區域。本例取中央區域，並在執行前檢查座標；不是自動尋找紙張。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

height, width = image.shape[:2]
x1, x2 = width // 4, 3 * width // 4
y1, y2 = height // 4, 3 * height // 4
if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
    raise ValueError("裁切範圍不合法")
crop = image[y1:y2, x1:x2].copy()

cv2.imshow("Original", image)
cv2.imshow("ROI", crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 位置描述 | 切片 |
| --- | --- |
| 左半邊 | `image[:, :width // 2]` |
| 右半邊 | `image[:, width // 2:]` |
| 上半邊 | `image[:height // 2, :]` |
| 指定矩形 | `image[y1:y2, x1:x2]` |

**練習：**先在紙上寫出希望保留的區域，再修改座標。請說出輸出高度和寬度應各是多少。

---

## 單元七｜縮放與插值

縮放要計算新的像素。`resize()` 的尺寸參數是 `(寬, 高)`，和 `shape` 的順序不同。

### 完整範例：固定比例縮小

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

small = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
print("原圖：", image.shape)
print("縮小：", small.shape)

cv2.imshow("Original", image)
cv2.imshow("Half size", small)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 新參數 | 意義 |
| --- | --- |
| `None` | 這次不直接指定輸出寬高，改用倍率 |
| `fx`、`fy` | 水平與垂直倍率；相同倍率保持比例 |
| `interpolation` | 新像素的取樣／估算方法 |

倍率只適用於輸出尺寸至少為 1 的圖片。本章測試圖片應至少為 32 × 32。

| 插值方式 | 特性與常見用途 |
| --- | --- |
| `INTER_NEAREST` | 最近鄰；保留離散值，放大像素格或遮罩 |
| `INTER_LINEAR` | 雙線性；較平滑，一般放大常用 |
| `INTER_CUBIC` | 較多鄰近取樣的三次插值；成本較高，不能補回不存在的細節 |
| `INTER_AREA` | 區域取樣，常用於縮小 |

**觀察：**縮小後細線可能變淡或消失，不能只用視窗看起來差不多，就認為資料沒改變。

---

## 單元八｜比較插值與固定寬度

把同一個小區域放大，較容易看到不同插值造成的差異。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

height, width = image.shape[:2]
x, y = width // 2, height // 2
patch = image[max(0, y - 20):y + 20, max(0, x - 20):x + 20].copy()
nearest = cv2.resize(patch, (400, 400), interpolation=cv2.INTER_NEAREST)
linear = cv2.resize(patch, (400, 400), interpolation=cv2.INTER_LINEAR)
cubic = cv2.resize(patch, (400, 400), interpolation=cv2.INTER_CUBIC)

cv2.imshow("Nearest", nearest)
cv2.imshow("Linear", linear)
cv2.imshow("Cubic", cubic)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`max(0, ...)` 避免索引變成負數。這個例子比較插值；原區域若不是正方形，強制放成 `(400, 400)` 會改變比例。

要固定寬度又保持比例，計算 `new_height = round(height * new_width / width)`，再呼叫 `resize(image, (new_width, new_height), ...)`。

**練習：**把一張寬 1200、高 800 的圖縮成寬 600，先算新高度。`reshape()` 能取代這裡的 `resize()` 嗎？

---

## 單元九｜翻轉

翻轉改變左右或上下方向，不是校正幾度的歪斜。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

horizontal = cv2.flip(image, 1)
vertical = cv2.flip(image, 0)
both = cv2.flip(image, -1)

cv2.imshow("Original", image)
cv2.imshow("Left right", horizontal)
cv2.imshow("Up down", vertical)
cv2.imshow("Both", both)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.flip(image, flipCode)` 回傳新影像。`1` 左右翻、`0` 上下翻、`-1` 同時翻。

**觀察：**含有文字的圖片最容易看出鏡像。不能為了方向看起來順眼，就任意將樂譜左右鏡像。

---

## 單元十｜補邊

補邊增加外圍畫布，不改變原物體大小。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

padded = cv2.copyMakeBorder(
    image, 30, 30, 50, 50,
    cv2.BORDER_CONSTANT, value=(255, 255, 255),
)

cv2.imshow("Original", image)
cv2.imshow("White border", padded)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

四個數字依序是「上、下、左、右」。BGR 白色用三個 `255`；灰階白色才是一個 `255`。

| 邊界模式 | 外圍如何產生 |
| --- | --- |
| `BORDER_CONSTANT` | 使用固定值 |
| `BORDER_REPLICATE` | 重複最外圍像素 |
| `BORDER_REFLECT` | 反射影像內容 |

白紙照片常用白色補邊，但不是所有場景都適用。邊界值也會影響後續濾波與偵測。

---

## 單元十一｜畫線

繪圖函式會改動傳入的陣列，所以先複製。畫出的線是標記，不是偵測結果。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

marked = image.copy()
height, width = image.shape[:2]
cv2.line(marked, (0, height // 2), (width - 1, height // 2), (0, 0, 255), 2)

cv2.imshow("Original", image)
cv2.imshow("Line", marked)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.line(影像, 起點, 終點, 顏色, 粗細)` 使用 `(x, y)` 座標。`2` 表示線條厚度為 2 像素。

**練習：**改成由左上角到右下角的線。寬度為 `width` 時，最右邊索引為何是 `width - 1`？

---

## 單元十二｜畫矩形

畫框能指出裁切範圍或候選物體位置。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

marked = image.copy()
height, width = image.shape[:2]
x1, x2 = width // 4, 3 * width // 4
y1, y2 = height // 4, 3 * height // 4
cv2.rectangle(marked, (x1, y1), (x2 - 1, y2 - 1), (0, 255, 0), 2)

cv2.imshow("Original", image)
cv2.imshow("Rectangle", marked)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.rectangle(影像, 左上角, 右下角, 顏色, 粗細)`。切片終點不包含，但繪圖端點可能包含，標示切片範圍時因此使用 `x2 - 1` 與 `y2 - 1`。

`thickness=-1` 表示填滿矩形，正整數表示邊框粗細。

---

## 單元十三｜畫圓

圓由中心與半徑決定，不是由兩個角點決定。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

marked = image.copy()
height, width = image.shape[:2]
radius = max(1, min(height, width) // 6)
cv2.circle(marked, (width // 2, height // 2), radius, (0, 0, 255), 2)

cv2.imshow("Original", image)
cv2.imshow("Circle", marked)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.circle(影像, 圓心, 半徑, 顏色, 粗細)`。`min(height, width)` 取較短邊，避免半徑大幅超出圖片。

**練習：**將粗細改成 `-1` 填滿，再和只畫外框的版本比較。

---

## 單元十四｜加入文字

使用英文標籤指出處理階段，方便比較視窗與結果。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

marked = image.copy()
cv2.putText(marked, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 0, 255), 2, cv2.LINE_AA)

cv2.imshow("Labeled", marked)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

| 新參數 | 意義 |
| --- | --- |
| `(10, 30)` | 文字基線起點，不是文字框左上角 |
| `FONT_HERSHEY_SIMPLEX` | OpenCV 內建字型 |
| `0.8` | 字型縮放比例 |
| `2` | 筆畫粗細 |
| `LINE_AA` | 抗鋸齒線條 |

內建 Hershey 字型不能直接完整顯示繁體中文，所以圖片標籤使用英文。這不限制 Python 的 `print()` 印中文。

| 繪圖函式 | 主要位置參數 |
| --- | --- |
| `line()` | 起點、終點 |
| `rectangle()` | 左上角、右下角 |
| `circle()` | 中心、半徑 |
| `putText()` | 文字基線起點 |

---

## 單元十五｜遮罩選取

裁切改變圖片尺寸；遮罩可保留原尺寸，指定哪些位置留下。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

import numpy as np

height, width = image.shape[:2]
mask = np.zeros((height, width), dtype=np.uint8)
cv2.circle(mask, (width // 2, height // 2), min(height, width) // 3, 255, -1)
selected = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow("Original", image)
cv2.imshow("Mask", mask)
cv2.imshow("Selected", selected)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.bitwise_and(a, b, mask=...)` 逐位元計算 AND。相同圖片和自己 AND，原值不變；遮罩非零的位置才寫入結果。這裡新結果的未選區域為黑色。

遮罩需要和圖片同寬高、單通道、`uint8`。白色代表「選中」，不代表原物體是白色。

---

## 單元十六｜另存結果

視窗顯示不等於存檔。需要保存時，使用不同路徑，避免覆蓋測試圖片。

### 完整範例

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
from pathlib import Path

output = Path("output")
output.mkdir(exist_ok=True)
path = output / "lesson05_gray.png"
if path.exists():
    raise FileExistsError("結果已存在，請更改輸出檔名後再執行")
ok = cv2.imwrite(str(path), gray)
if not ok:
    raise OSError("寫入圖片失敗")
print("已儲存：", path)

cv2.imshow("Gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`Path` 的基本操作已在第 3 章介紹。`cv2.imwrite(檔名, 圖片)` 依副檔名選擇編碼，回傳是否成功；部分錯誤也會提出 `cv2.error`。`str(path)` 將路徑物件轉成 OpenCV 接受的文字。

這是單人本機練習的同名檔檢查，不是防止其他程式同時寫檔的完整機制。PNG 適合保留中間像素結果；JPEG 是有損壓縮，反覆儲存可能改變細線與邊緣。

### 中文路徑讀不到時

先排除工作目錄與檔名問題。部分 OpenCV／平台組合可能需要把「讀取位元組」與「影像解碼」分開，以下不需要自訂函式。

```python
import cv2
import numpy as np
from pathlib import Path

raw = Path("test.jpg").read_bytes()
if not raw:
    raise ValueError("圖片檔案是空的")
encoded = np.frombuffer(raw, dtype=np.uint8)
image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
if image is None:
    raise ValueError("檔案內容不是可解碼的圖片")

cv2.imshow("Decoded", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`read_bytes()` 讀出檔案位元組，`frombuffer()` 將它交成數值緩衝區，`imdecode()` 才把壓縮內容解碼成像素。不能直接把位元組陣列當圖片。

---

## 綜合實作｜框選、裁切、縮小與灰階比較

### 引導思考

先讀圖取得尺寸，再決定 ROI。畫框使用副本，裁切仍用未畫框的原圖。裁切後等比例縮小，再轉灰階；比較時把灰階複製成三通道，才能與彩圖拼接。

### 完整程式：`lesson05_compare.py`

```python
import cv2

image = cv2.imread("test.jpg")
if image is None:
    raise FileNotFoundError("讀不到 test.jpg，請檢查檔名與工作目錄")

import numpy as np

height, width = image.shape[:2]
x1, x2 = width // 4, 3 * width // 4
y1, y2 = height // 4, 3 * height // 4
if x1 >= x2 or y1 >= y2:
    raise ValueError("圖片太小，無法裁切中央區域")

marked = image.copy()
cv2.rectangle(marked, (x1, y1), (x2 - 1, y2 - 1), (0, 0, 255), 2)
crop = image[y1:y2, x1:x2].copy()
crop_h, crop_w = crop.shape[:2]
new_w = min(500, crop_w)
new_h = max(1, round(crop_h * new_w / crop_w))
small = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
comparison = np.hstack([small, gray_bgr])
print("ROI 座標：", x1, y1, x2, y2)
print("縮小後：", small.shape)

cv2.imshow("ROI on original", marked)
cv2.imshow("Color - Gray", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 觀察與修改

框線應正確包住裁出的區域，框線不應出現在裁切後的圖片裡。左右比較圖尺寸相同，右側少了顏色，但不是黑白二值圖。

把 ROI 改成上半部，然後用 `putText()` 標示原圖與灰階。最後自行加入另存 PNG 的步驟，不能使用 `test.jpg` 當輸出檔名。

### 自我檢查

1. 單一藍通道直接顯示，為什麼沒有藍色？
2. BGR 轉 RGB 後直接交給 `imshow()` 會怎樣？
3. 裁切、縮放、調整視窗與補邊有什麼不同？
4. 哪些函式會直接改動輸入陣列？
5. 圖片在視窗看得到，是否就代表已經寫入檔案？

## 延伸閱讀

- [OpenCV：影像基本操作](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html)
- [OpenCV：幾何轉換](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)
- [OpenCV：繪圖函式](https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html)
