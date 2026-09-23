# 第 4 章｜NumPy 與數位影像

影像可以看成一張由數值組成的表格。改變數值，就能改變亮度；選取一段範圍，就能裁切；比較數值，就能找出符合條件的位置。

本章先用小陣列觀察運算，再把相同操作放到一張較大的影像上。先理解資料如何改變，後面使用影像處理函式時，才知道應該檢查什麼。

## 學習目標

- 分辨像素、通道、陣列維度與資料型別。
- 建立陣列，使用索引、切片、遮罩與複製。
- 正確處理 `uint8` 的範圍、亮度調整與正規化。
- 使用廣播、統計與影像拼接。
- 完成一支建立、裁切、調整與分析影像的程式。

[TOC]

---

## 練習方式

本章使用第 1 章建立的 **Python 3.11** 環境，不需要重新安裝或更換套件。

每個 Python 程式區塊都是完整的小範例，可以各自存成 `.py` 執行；不需要保留上一個區塊的變數。最後的整合範例另存成 `lesson04_array_lab.py`。

先手算或預測結果，再執行比較。陣列範例使用自行建立的資料，不需要另外下載照片。

---

## 單元一｜像素與灰階

### 1-1｜一個像素保存什麼？

像素是影像網格中的一個位置。對本章使用的 8 位元灰階影像，一個像素保存 `0～255` 的灰階值：`0` 表示黑色，`255` 表示白色，中間的數字表示不同深淺。

這是特定影像表示法的範圍，不代表所有圖片都只能使用 8 位元。

### 範例：用數字畫出黑色方塊

```python
import numpy as np

image = np.array([
    [255, 255, 255, 255],
    [255,   0,   0, 255],
    [255,   0,   0, 255],
    [255, 255, 255, 255],
], dtype=np.uint8)

print(image)
print("左上角：", image[0, 0])
print("中央：", image[1, 1])
```

**觀察：**中間四個數值為 `0`，形成黑色方塊；外圈為 `255`。把中央的 `0` 改成 `128`，形狀沒有改變，但顏色會變成灰色。

### 思考

一張 `4 × 4` 灰階影像有 16 個像素。若每個像素占一個位元組，像素陣列需要多少位元組？它與儲存成 PNG 後的檔案大小會相同嗎？

---

## 單元二｜建立陣列與調整形狀

### 2-1｜常用建立方式

`np.array()` 由既有資料建立陣列；`np.zeros()` 建立全零陣列；`np.ones()` 建立全一陣列；`np.full()` 將所有元素設成指定值。

對 `uint8` 圖片，全一陣列的灰階是 `1`，接近黑色，不是白色。

### 範例：建立不同畫布

```python
import numpy as np

black = np.zeros((3, 5), dtype=np.uint8)
near_black = np.ones((3, 5), dtype=np.uint8)
white = np.full((3, 5), 255, dtype=np.uint8)

print("黑色畫布：\n", black)
print("全一畫布：\n", near_black)
print("白色畫布：\n", white)
```

**觀察：**`(3, 5)` 表示 3 列、5 欄，也就是高度 3、寬度 5。

### 2-2｜`arange()`、`linspace()` 與 `reshape()`

`arange()` 依步長建立數列，通常不包含終點；`linspace()` 依指定個數等距取樣，預設包含兩端。`reshape()` 重新安排形狀，但不增加或刪除元素。

### 範例：數列變成表格

```python
import numpy as np

numbers = np.arange(12, dtype=np.int16)
grid = numbers.reshape(3, 4)
levels = np.linspace(0, 255, 6)

print(numbers)
print(grid)
print(levels)
print("元素數量：", numbers.size, grid.size)
```

`grid` 應為：

```text
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

把 12 個元素改成 `reshape(2, 7)` 會失敗，因為新形狀需要 14 個元素。`reshape()` 不是圖片縮放，不能用它把照片拉寬。

---

## 單元三｜`shape`、`ndim`、`size` 與 `dtype`

灰階影像常見形狀是 `(高度, 寬度)`，三通道彩圖則是 `(高度, 寬度, 3)`。

| 屬性 | 意義 |
| --- | --- |
| `shape` | 每個維度的長度 |
| `ndim` | 維度數量 |
| `size` | 所有陣列元素的總數 |
| `dtype` | 每個元素的資料型別 |
| `nbytes` | 陣列元素占用的位元組數 |

### 範例：像素數不等於彩圖的 `size`

```python
import numpy as np

gray = np.zeros((3, 5), dtype=np.uint8)
color = np.zeros((3, 5, 3), dtype=np.uint8)

for name, image in [("gray", gray), ("color", color)]:
    height, width = image.shape[:2]
    print(name)
    print("shape：", image.shape)
    print("ndim：", image.ndim)
    print("像素數：", height * width)
    print("元素數：", image.size)
    print("dtype：", image.dtype)
    print("位元組數：", image.nbytes)
```

兩張圖都有 15 個像素，但彩圖有 45 個通道元素。`nbytes` 只計算陣列資料，不包含 Python 物件管理成本，也不是壓縮後的圖檔大小。

---

## 單元四｜座標、索引與修改像素

影像左上角是原點，`x` 向右增加，`y` 向下增加。

```text
幾何座標：       (x, y)
NumPy 灰階索引： image[y, x]
彩圖通道索引：   image[y, x, channel]
```

### 範例：找出指定位置

```python
import numpy as np

image = np.arange(20, dtype=np.uint8).reshape(4, 5)
x, y = 3, 1

print(image)
print("座標 (3, 1)：", image[y, x])
print("最後一個像素：", image[-1, -1])
image[y, x] = 200
print("修改後：\n", image)
```

原本 `(3, 1)` 的值是 `8`。寬度為 5 的影像，合法 `x` 索引是 `0～4`，不是 `1～5`。

### 小練習

建立 `6 × 8` 的黑色畫布，將 `(x=5, y=2)` 設成白色。再讓第 0 列全部變成灰色。操作前先指出程式中的哪個數字代表列、哪個代表欄。

---

## 單元五｜切片、裁切與複製

### 5-1｜切片範圍

`image[y1:y2, x1:x2]` 選取矩形區域。起點包含，終點不包含，因此區域高度是 `y2-y1`，寬度是 `x2-x1`。

### 範例：裁出中央區域

```python
import numpy as np

image = np.arange(48, dtype=np.uint8).reshape(6, 8)
crop = image[2:4, 3:6].copy()

print(crop)
print("裁切形狀：", crop.shape)
print("前兩列：\n", image[:2, :])
print("每隔一欄取樣：\n", image[:, ::2])
```

中央區域應是 `[[19, 20, 21], [27, 28, 29]]`，形狀為 `(2, 3)`。`::2` 是抽取元素，不等於具有抗混疊處理的影像縮小。

### 5-2｜切片通常共用原資料

NumPy 的基本切片產生 **view**，也就是指向原資料的一個視圖。修改視圖可能同時改變原圖。需要獨立修改時，使用 `.copy()`。

### 範例：比較視圖與複本

```python
import numpy as np

image = np.full((4, 6), 255, dtype=np.uint8)
view = image[1:3, 2:4]
copy = image[1:3, 2:4].copy()

view[0, 0] = 0
copy[1, 1] = 80

print("原圖受 view 影響：", image[1, 2])
print("原圖不受 copy 影響：", image[2, 3])
print("是否共用資料：", np.shares_memory(image, view))
print("是否共用資料：", np.shares_memory(image, copy))
```

**觀察：**前兩行分別輸出 `0` 與 `255`。單純寫 `another = image` 也不會複製圖片。

---

## 單元六｜逐元素運算與溢位

### 6-1｜NumPy 運算作用在對應元素

同形狀陣列的 `+`、`-`、`*` 是逐元素運算。`*` 不是矩陣乘法；矩陣乘法使用 `@`，本章不需要它。

### 範例：逐元素加法

```python
import numpy as np

a = np.array([[10, 20], [30, 40]], dtype=np.int16)
b = np.array([[1, 2], [3, 4]], dtype=np.int16)

print(a + b)
print(a * b)
```

### 6-2｜`uint8` 不會自動保存超過範圍的答案

`uint8` 只能表示 `0～255`。下面刻意使用相同型別的陣列相加，觀察固定寬度整數的回繞：`250+10=260`，存回 8 位元無號整數後變成 `4`。

### 範例：直接加法與裁切範圍

```python
import numpy as np

values = np.array([0, 100, 250, 255], dtype=np.uint8)
addition = np.full_like(values, 10)
wrapped = values + addition
safe = np.clip(values.astype(np.int16) + 10, 0, 255).astype(np.uint8)

print("直接相加：", wrapped)
print("限制範圍：", safe)
```

預期結果：

```text
直接相加： [ 10 110   4   9]
限制範圍： [ 10 110 255 255]
```

先轉成能容納中間結果的型別，再運算、限制範圍，最後轉回 `uint8`。不是先溢位之後再呼叫 `clip()`，因為錯誤結果已經發生。

---

## 單元七｜亮度調整與正規化

### 7-1｜加上常數調整亮度

將每個像素加上正數，通常會變亮；減去數值則變暗。超過範圍的部分會被截斷，因此這不是可逆的操作。

### 範例：建立較亮與較暗的陣列

```python
import numpy as np

image = np.array([[20, 80, 140, 220]], dtype=np.uint8)
work = image.astype(np.float32)
brighter = np.clip(work + 40, 0, 255).astype(np.uint8)
darker = np.clip(work - 40, 0, 255).astype(np.uint8)

print("原始：", image)
print("變亮：", brighter)
print("變暗：", darker)
```

`220+40` 變成 `255`，`20-40` 變成 `0`。一旦不同亮度被壓到相同的端點，原本的細節就不能只靠相反運算完整找回。

### 7-2｜將數值表示成 `0～1`

正規化可以改變資料的數值表示，並不一定改變顯示出來的亮暗關係。

### 範例：正規化再還原

```python
import numpy as np

image = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
normalized = image.astype(np.float32) / 255.0
restored = np.rint(normalized * 255).clip(0, 255).astype(np.uint8)

print(normalized)
print(normalized.dtype)
print("還原一致：", np.array_equal(image, restored))
```

`.astype(np.uint8)` 只是轉型，不會自動把 `0～1` 放大成 `0～255`。OpenCV 各函式接受的型別不同，不能認為轉成浮點數之後所有函式都能直接使用。

---

## 單元八｜布林遮罩與條件選取

### 8-1｜用條件產生一張真假表

`image < 100` 會逐像素比較，得到與原灰階圖同形狀的布林陣列。

### 範例：標記較暗的區域

```python
import numpy as np

image = np.array([[20, 120, 220], [50, 150, 250]], dtype=np.uint8)
mask = image < 100
result = image.copy()
result[mask] = 0
binary = np.where(mask, 255, 0).astype(np.uint8)

print("遮罩：\n", mask)
print("選到的數值：", image[mask])
print("修改後：\n", result)
print("白色表示選中：\n", binary)
```

`image[mask]` 將選中的元素取出成一維資料；`result[mask] = 0` 則是修改原位置。不要把「取出資料」和「保留原影像形狀」混為一談。

### 8-2｜合併多個條件

NumPy 逐元素邏輯使用 `&`、`|`、`~`，條件各自加括號；Python 的 `and`、`or` 不用來合併整張布林陣列。

### 範例：選取中間亮度

```python
import numpy as np

image = np.array([[20, 80, 120, 180, 240]], dtype=np.uint8)
mask = (image >= 80) & (image <= 180)

print(mask)
print("選中數量：", np.count_nonzero(mask))
print("至少一個：", mask.any())
print("全部符合：", mask.all())
```

---

## 單元九｜彩色通道與通道操作

### 9-1｜RGB 與 BGR 是排列約定

三通道陣列本身不記得自己是 RGB 還是 BGR，必須由讀取、處理與顯示方式共同約定。OpenCV 常用 BGR；Matplotlib 顯示彩圖時使用 RGB。

### 範例：建立 BGR 色塊與取出單一通道

```python
import numpy as np

image = np.zeros((2, 3, 3), dtype=np.uint8)
image[:, 0] = (255, 0, 0)  # BGR：藍
image[:, 1] = (0, 255, 0)  # BGR：綠
image[:, 2] = (0, 0, 255)  # BGR：紅

blue = image[:, :, 0]
red_only = np.zeros_like(image)
red_only[:, :, 2] = image[:, :, 2]
rgb = image[:, :, ::-1].copy()

print("原圖形狀：", image.shape)
print("藍通道形狀：", blue.shape)
print("藍通道：\n", blue)
print("第一列 RGB：\n", rgb[0])
```

單一通道是二維數值表，直接用灰階顯示時不會自動變藍。要顯示「只保留藍光的彩圖」，需要保留三個通道，再將其他通道設成零。

### 9-2｜合併通道

### 範例：用 `stack()` 組回彩圖

```python
import numpy as np

blue = np.full((2, 4), 200, dtype=np.uint8)
green = np.full((2, 4), 100, dtype=np.uint8)
red = np.zeros((2, 4), dtype=np.uint8)
image = np.stack([blue, green, red], axis=2)

print(image.shape)
print(image[0, 0])
```

`axis=2` 在第三個維度疊出通道，結果是 `(2, 4, 3)`。各通道需要具有相同高寬。

---

## 單元十｜廣播：用較小陣列處理整張圖

廣播讓形狀相容的陣列進行逐元素運算。判斷時從最後一個維度往前看：長度相等，或其中一個長度為 `1`，才可以配合。

### 範例：建立由左到右的漸層

```python
import numpy as np

row = np.linspace(0, 255, 8, dtype=np.float32)[None, :]
gradient = np.ones((4, 1), dtype=np.float32) * row
image = np.rint(gradient).astype(np.uint8)

print("row：", row.shape)
print("結果：", image.shape)
print(image)
```

`None` 在索引中新增一個長度為 `1` 的維度。`(4, 1)` 與 `(1, 8)` 相乘，得到 `(4, 8)`。

### 範例：每個通道加不同數值

```python
import numpy as np

image = np.full((2, 4, 3), 100, dtype=np.uint8)
offset = np.array([20, 0, -20], dtype=np.float32)
result = np.clip(image.astype(np.float32) + offset, 0, 255).astype(np.uint8)

print(result[0, 0])
print(result.shape)
```

結果像素是 `[120, 100, 80]`。這是通道偏移，不等於自動白平衡。

---

## 單元十一｜影像統計與直方圖

### 11-1｜總體統計與指定軸

最小值、最大值與平均值能幫忙檢查數值範圍，但不能單獨判定照片品質。完全白色的影像平均值很高，卻可能沒有任何有效內容。

### 範例：整張、每列與每欄的平均

```python
import numpy as np

image = np.array([[0, 100, 200], [50, 150, 250]], dtype=np.uint8)

print("最小、最大：", image.min(), image.max())
print("整體平均：", image.mean())
print("每欄平均：", image.mean(axis=0))
print("每列平均：", image.mean(axis=1))
```

`axis=0` 把列這個維度彙整掉，留下每欄結果；`axis=1` 把欄彙整掉，留下每列結果。

### 11-2｜直方圖記錄各亮度的數量

### 範例：統計灰階分布

```python
import numpy as np

image = np.array([[0, 0, 100], [100, 255, 255]], dtype=np.uint8)
histogram = np.bincount(image.ravel(), minlength=256)

for level in [0, 100, 255]:
    print(level, "出現", int(histogram[level]), "次")
print("總數正確：", int(histogram.sum()) == image.size)
```

`ravel()` 將資料攤平成一維；`bincount()` 適合統計非負整數。後面的 Otsu 二值化會利用灰階分布決定門檻，但直方圖本身沒有保存像素位置。

---

## 單元十二｜拼接與儲存觀察圖

相同高度的灰階圖可以沿 `axis=1` 左右拼接；上下拼接則沿 `axis=0`，且寬度必須相同。彩圖還需要通道數一致。

### 範例：原圖、反相圖左右比較

```python
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

image = np.tile(np.arange(256, dtype=np.uint8), (80, 1))
inverted = 255 - image
comparison = np.concatenate([image, inverted], axis=1)

output = Path(__file__).resolve().parent / "output" / "lesson04"
output.mkdir(parents=True, exist_ok=True)
plt.imsave(output / "gradient_comparison.png", comparison,
           cmap="gray", vmin=0, vmax=255)
print("輸出形狀：", comparison.shape)
print("已儲存：", output / "gradient_comparison.png")
```

本章用 Matplotlib 存觀察圖，不開啟桌面視窗。`Agg` 是可直接輸出圖片的繪圖後端。`vmin=0, vmax=255` 固定黑白範圍，避免每張灰階圖自動調整顯示而誤導比較。

Matplotlib 的 `imsave()` 可能將灰階資料寫成彩色或含透明通道的 PNG，所以這裡的輸出用於觀察，不用來驗證原陣列的通道數。下一章會用 OpenCV 保留明確的影像編碼。

重跑這個範例會更新 `output/lesson04/gradient_comparison.png`，不會更改外部輸入檔。

---

## 綜合實作｜建立一張影像實驗卡

### 一、先拆解問題

目標是用陣列建立影像，不讀取現成圖片，然後完成裁切、亮度調整、條件選取與統計。

先回答：畫布高寬是多少？矩形的座標範圍如何表示？哪些操作要保留原圖？左右拼圖時，各張圖的形狀是否一致？

```text
建立灰階漸層
    ↓
加入黑色矩形與細線
    ↓
複製原圖，調整亮度
    ↓
建立暗色區域遮罩
    ↓
拼接比較、裁切局部、輸出統計
```

### 二、完整程式

存成 **`lesson04_array_lab.py`**。每次執行建立新的輸出資料夾，保留之前的實驗結果。

```python
from pathlib import Path
from tempfile import mkdtemp
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent


def make_image():
    row = np.linspace(80, 240, 400, dtype=np.float32)[None, :]
    image = np.rint(np.ones((200, 1)) * row).astype(np.uint8)
    image[50:110, 50:150] = 20
    for y in [135, 145, 155, 165, 175]:
        image[y:y + 1, 30:370] = 0
    return image


def brighten(image, amount):
    return np.clip(image.astype(np.float32) + amount, 0, 255).astype(np.uint8)


def main():
    original = make_image()
    before = original.copy()
    brighter = brighten(original, 30)
    mask = np.where(original < 60, 255, 0).astype(np.uint8)
    crop = original[40:120, 40:160].copy()
    comparison = np.concatenate([original, brighter, mask], axis=1)

    output_root = BASE_DIR / "output" / "lesson04"
    output_root.mkdir(parents=True, exist_ok=True)
    run_dir = Path(mkdtemp(prefix="run_", dir=str(output_root)))

    for name, image in {"comparison": comparison, "crop": crop}.items():
        plt.imsave(run_dir / f"{name}.png", image,
                   cmap="gray", vmin=0, vmax=255)

    histogram = np.bincount(original.ravel(), minlength=256)
    info = {
        "shape": list(original.shape),
        "dtype": str(original.dtype),
        "minimum": int(original.min()),
        "maximum": int(original.max()),
        "mean": float(original.mean()),
        "dark_pixels": int(np.count_nonzero(original < 60)),
        "crop_shape": list(crop.shape),
        "histogram_total": int(histogram.sum()),
        "original_unchanged": bool(np.array_equal(original, before)),
    }
    (run_dir / "info.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(info, ensure_ascii=False, indent=2))
    print("輸出位置：", run_dir)


if __name__ == "__main__":
    main()
```

### 三、結果觀察

`comparison.png` 由左到右是原圖、加亮圖、暗色區域遮罩。原圖形狀為 `(200, 400)`，裁切結果為 `(80, 120)`，拼接結果為 `(200, 1200)`。

黑色矩形包含 `60 × 100 = 6000` 個像素，五條細線共有 `5 × 340 = 1700` 個像素，互不重疊，因此暗色像素應為 **7700**。`original_unchanged` 應為 `true`。

### 四、修改與推理

1. 將矩形改成 `image[50:110, 50:151]`，先預測暗色像素增加多少，再執行。
2. 將加亮數值從 `30` 改成 `80`，觀察哪些區域失去亮度差異。
3. 將遮罩條件改成 `original < 100`，說明為什麼部分背景也被選中。
4. 增加每列暗色像素數量，找出細線所在列。這只能找到影像結構，還不能證明那就是某種音樂符號。

---

## 章末自我檢查

能否解釋 `(200, 400, 3)` 的每個數字？能否在運算前預測裁切形狀？能否說明 `.copy()`、`astype()` 與 `clip()` 各自解決什麼問題？能否區分影像陣列的像素數、元素數與檔案大小？

## 與後續專題的連結

五線、文字與音符都是像素排列。後面裁切樂譜、統計前景、建立遮罩與估計方向，都會使用本章的陣列操作。

## 延伸閱讀

- [NumPy 1.26：陣列建立](https://numpy.org/doc/1.26/user/basics.creation.html)
- [NumPy 1.26：索引與切片](https://numpy.org/doc/1.26/user/basics.indexing.html)
- [NumPy 1.26：資料型別](https://numpy.org/doc/1.26/user/basics.types.html)
- [NumPy 1.26：廣播](https://numpy.org/doc/1.26/user/basics.broadcasting.html)
