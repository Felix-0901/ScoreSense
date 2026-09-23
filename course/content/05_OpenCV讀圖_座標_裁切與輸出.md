# 第 5 章｜OpenCV：讀圖、座標、裁切與輸出

NumPy 負責操作影像陣列，OpenCV 則提供影像解碼、色彩轉換、縮放、繪圖與編碼等功能。

本章使用色塊與細線練習。這些素材的位置與顏色已知，容易分辨處理結果是正確，還是只是「看起來像一張圖」。

## 學習目標

- 正確讀取與寫出圖片，分辨路徑、位元組與像素。
- 分辨 BGR、RGB、灰階與透明通道。
- 完成裁切、縮放、翻轉、補邊、繪圖與遮罩合成。
- 保留原圖，建立可追查的處理輸出。

[TOC]

---

## 範例準備｜共用素材與讀寫工具

沿用 **Python 3.11** 與第 1 章的環境。本章不使用 `cv2.imshow()`，處理結果存成圖片後，用圖片檢視器或 VS Code 開啟；不需要為了開視窗更換 OpenCV 套件。

先將下列完整程式存成 **`lesson05_common.py`**。後面的短範例各自存成另一支 `.py`，與它放在同一個資料夾。匯入共用工具後，每段範例可獨立執行，不需要按照順序累積變數。

```text
scoresense_course/
├── lesson05_common.py
├── lesson05_practice.py
└── output/
```

`make_demo()` 產生 `240 × 400` 的 BGR 色塊圖；`new_run()` 每次建立新的輸出目錄；`save_png()` 只建立新檔，不覆蓋同名檔案。讀寫細節會在單元一、二說明。

```python
from pathlib import Path
from tempfile import mkdtemp
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent


def new_run(label):
    root = BASE_DIR / "output" / "lesson05"
    root.mkdir(parents=True, exist_ok=True)
    return Path(mkdtemp(prefix=f"{label}_", dir=str(root)))


def make_demo():
    image = np.full((240, 400, 3), 245, dtype=np.uint8)
    image[30:120, 30:130] = (255, 0, 0)
    image[30:120, 150:250] = (0, 255, 0)
    image[30:120, 270:370] = (0, 0, 255)
    for y in range(155, 206, 10):
        image[y:y + 2, 30:370] = (20, 20, 20)
    return image


def read_bgr(path):
    path = Path(path)
    raw = path.read_bytes()
    if not raw:
        raise ValueError(f"檔案是空的：{path.name}")
    image = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"無法解碼圖片：{path.name}")
    return image


def save_png(path, image):
    path = Path(path)
    if path.suffix.lower() != ".png":
        raise ValueError("輸出檔名必須以 .png 結尾")
    if image.dtype != np.uint8 or image.size == 0:
        raise ValueError("需要非空的 uint8 影像")
    if image.ndim not in (2, 3):
        raise ValueError("影像必須是二維或三維")
    if image.ndim == 3 and image.shape[2] not in (3, 4):
        raise ValueError("彩圖需要 3 或 4 個通道")
    ok, buffer = cv2.imencode(".png", np.ascontiguousarray(image))
    if not ok:
        raise ValueError("PNG 編碼失敗")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as file:
        file.write(buffer.tobytes())
```

每個短範例最後會印出輸出位置。這些練習只處理自行建立的圖片；讀真實照片時，將範例中的素材產生步驟換成 `read_bgr(照片路徑)`，不要將輸出路徑設成原照片路徑。

---

## 單元一｜讀取圖片：檔案不等於陣列

### 1-1｜一般路徑讀取

`cv2.imread()` 依圖片內容解碼，並回傳陣列。`IMREAD_COLOR` 取得三通道 BGR 圖片；`IMREAD_GRAYSCALE` 取得灰階圖；`IMREAD_UNCHANGED` 盡量保留原始通道與深度。

### 範例：將已知陣列存檔再讀回

```python
import cv2
import numpy as np
from lesson05_common import make_demo, new_run, save_png

run = new_run("read")
source = run / "source.png"
original = make_demo()
save_png(source, original)
image = cv2.imread(str(source), cv2.IMREAD_COLOR)
if image is None:
    raise ValueError("讀取失敗，請檢查檔案與路徑")
print("形狀：", image.shape)
print("內容一致：", np.array_equal(original, image))
print(run)
```

預期形狀為 `(240, 400, 3)`，PNG 讀回的像素與原陣列一致。檔案不存在、無法存取或內容不能解碼，都可能造成 `None`，不能直接接著存取 `.shape`。

### 1-2｜由位元組解碼，處理中文路徑

`Path.read_bytes()` 負責讀檔，`np.frombuffer()` 將位元組看成數值緩衝區，`cv2.imdecode()` 再把編碼內容解成像素。讀到位元組不等於圖片已經解碼成功。

### 範例：中文資料夾與檔名

```python
from lesson05_common import make_demo, new_run, save_png, read_bgr

run = new_run("unicode")
path = run / "圖片練習" / "色塊.png"
save_png(path, make_demo())
image = read_bgr(path)
print("讀取成功：", image.shape)
print(run)
```

`read_bgr()` 採用這條讀取流程，並區分空檔與無法解碼。副檔名只是線索，將文字改名成 `.png` 不會讓它變成圖片。

### 1-3｜直接讀取灰階

### 範例：灰階讀取與彩圖轉灰階

```python
import cv2
import numpy as np
from lesson05_common import make_demo, new_run, save_png

run = new_run("gray_read")
path = run / "source.png"
save_png(path, make_demo())
raw = np.frombuffer(path.read_bytes(), dtype=np.uint8)
gray = cv2.imdecode(raw, cv2.IMREAD_GRAYSCALE)
if gray is None:
    raise ValueError("灰階解碼失敗")
save_png(run / "gray.png", gray)
print(gray.shape, gray.dtype)
print(run)
```

灰階結果形狀為 `(240, 400)`。直接以灰階解碼和先讀彩圖再 `cvtColor()`，可能因解碼器換算方式而產生些微數值差異；比較結果時要固定讀取方式。

---

## 單元二｜寫出圖片與保存原圖

### 2-1｜`imwrite()` 的回傳值

`cv2.imwrite()` 由輸出副檔名選擇編碼器。父資料夾需要先存在，回傳值應檢查；部分錯誤也可能直接提出 `cv2.error`。

### 範例：儲存並驗證 PNG

```python
import cv2
from lesson05_common import make_demo, new_run

run = new_run("imwrite")
path = run / "result.png"
if not cv2.imwrite(str(path), make_demo()):
    raise OSError("圖片寫入失敗")
print("檔案存在：", path.is_file())
print("檔案大小：", path.stat().st_size)
print(run)
```

`imwrite()` 可能覆寫同名檔。範例先建立新資料夾，因此不會覆蓋之前的輸出。

共用的 `save_png()` 則先用 `imencode()` 得到 PNG 位元組，再以 `"xb"` 建立新檔。它不負責自動選擇新檔名，同名檔存在時會明確失敗。

### 2-2｜PNG 與 JPEG 的差異

PNG 適合保存需要保留像素的中間結果；JPEG 常用於照片，通常是有損壓縮。JPEG 反覆存取可能增加壓縮誤差，細線附近也可能出現額外紋理。

### 範例：比較同一張圖的編碼與還原

```python
import cv2
import numpy as np
from lesson05_common import make_demo, new_run, save_png

run = new_run("codec")
image = make_demo()
for ext, params in [(".png", []), (".jpg", [cv2.IMWRITE_JPEG_QUALITY, 60])]:
    ok, buffer = cv2.imencode(ext, image, params)
    if not ok:
        raise ValueError("編碼失敗")
    with (run / f"encoded{ext}").open("xb") as file:
        file.write(buffer.tobytes())
    decoded = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if decoded is None:
        raise ValueError("解碼失敗")
    error = np.abs(decoded.astype(np.int16) - image.astype(np.int16))
    print(ext, "位元組數：", buffer.size, "平均絕對誤差：", float(error.mean()))
    save_png(run / f"decoded_{ext[1:]}.png", decoded)
print(run)
```

PNG 的誤差應為零；此色塊範例的 JPEG 通常不為零。檔案較小不代表影像資訊保留得更完整。這是編碼誤差比較，不是辨識準確率。

---

## 單元三｜BGR、RGB 與灰階轉換

### 3-1｜BGR 轉 RGB 後再交給 Matplotlib

### 範例：正確顯示色塊

```python
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lesson05_common import make_demo, new_run

run = new_run("rgb")
bgr = make_demo()
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
plt.imsave(run / "correct_rgb.png", rgb)
plt.imsave(run / "wrong_order.png", bgr)
print(run)
```

正確圖片左邊是藍色，右邊是紅色；通道順序錯誤會讓紅藍互換。`cvtColor()` 回傳新陣列，不會因為呼叫過就自動修改原本的 `bgr`。

### 3-2｜彩圖轉灰階

對常見 8 位元 BGR 圖片，灰階近似由 `0.114B + 0.587G + 0.299R` 計算，不是三個通道直接取平均；整數結果也包含取整。

### 範例：比較三個色塊的灰階

```python
import cv2
from lesson05_common import make_demo, new_run, save_png

run = new_run("gray")
image = make_demo()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
save_png(run / "original.png", image)
save_png(run / "gray.png", gray)
print("藍、綠、紅的灰階：", [int(gray[60, x]) for x in (60, 180, 300)])
print(run)
```

結果約為 `29、150、76`。綠色比藍色亮，是換算權重不同，不是讀圖錯誤。

### 3-3｜分離與合併通道

### 範例：單通道灰階與保留單一顏色

```python
import cv2
import numpy as np
from lesson05_common import make_demo, new_run, save_png

run = new_run("channels")
image = make_demo()
b, g, r = cv2.split(image)
zeros = np.zeros_like(b)
blue_only = cv2.merge([b, zeros, zeros])
restored = cv2.merge([b, g, r])
save_png(run / "blue_as_gray.png", b)
save_png(run / "blue_only.png", blue_only)
print("合併後一致：", np.array_equal(image, restored))
print(run)
```

`blue_as_gray.png` 顯示藍通道數值的亮暗；`blue_only.png` 才是保留藍色通道的彩圖。

---

## 單元四｜透明通道與白色背景合成

四通道 PNG 常包含 alpha 透明度。`IMREAD_UNCHANGED` 可能得到 BGRA，不應直接假定所有圖片都是三通道。

對本例的非預乘（straight）alpha，合成公式是 `結果 = 原色 × alpha + 背景色 × (1-alpha)`，alpha 先轉成 `0～1`。直接丟棄透明通道不等於合成白底。

### 範例：半透明紅色疊在白底

```python
import cv2
import numpy as np
from lesson05_common import new_run, save_png

run = new_run("alpha")
bgra = np.zeros((100, 160, 4), dtype=np.uint8)
bgra[:, :, 2] = 255
bgra[:, :, 3] = 128
save_png(run / "transparent.png", bgra)
raw = np.frombuffer((run / "transparent.png").read_bytes(), dtype=np.uint8)
loaded = cv2.imdecode(raw, cv2.IMREAD_UNCHANGED)
if loaded is None or loaded.ndim != 3 or loaded.shape[2] != 4:
    raise ValueError("需要四通道圖片")
alpha = loaded[:, :, 3:4].astype(np.float32) / 255.0
composite = loaded[:, :, :3].astype(np.float32) * alpha + 255 * (1 - alpha)
composite = np.rint(composite).clip(0, 255).astype(np.uint8)
save_png(run / "on_white.png", composite)
print("白底合成 BGR：", composite[0, 0])
print(run)
```

結果應接近 `[127, 127, 255]`，看起來是淡紅色。這個計算用來理解透明度；嚴格的色彩管理還涉及色彩空間與 gamma，不是只靠這個式子就全部完成。

---

## 單元五｜ROI 裁切與邊界檢查

ROI 是感興趣區域。裁切保留指定矩形中的像素，並不自動辨識其中的物體。

### 範例：裁出第一個色塊

```python
import cv2
from lesson05_common import make_demo, new_run, save_png

run = new_run("crop")
image = make_demo()
h, w = image.shape[:2]
x1, y1, x2, y2 = 20, 20, 140, 130
if not (0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
    raise ValueError("裁切範圍不合法")
crop = image[y1:y2, x1:x2].copy()
marked = image.copy()
cv2.rectangle(marked, (x1, y1), (x2 - 1, y2 - 1), (0, 0, 255), 2)
save_png(run / "marked.png", marked)
save_png(run / "crop.png", crop)
print("裁切形狀：", crop.shape)
print(run)
```

結果形狀為 `(110, 120, 3)`。切片終點不包含，但繪圖端點可能包含，所以框線右下角使用 `x2-1、y2-1`。

NumPy 切片超過邊界不一定報錯，有時會變成較小陣列或空陣列。因此應先驗證範圍，不能只以「沒有例外」判定裁切正確。

### 修改練習

裁出下半部細線區域，並在原圖副本上畫出框線。解釋為什麼畫框不能直接改動稍後還要處理的原圖。

---

## 單元六｜縮放與插值

### 6-1｜固定尺寸與維持比例

`cv2.resize(image, (new_width, new_height))` 的尺寸順序是**寬、高**，與陣列 `shape` 的高、寬相反。

### 範例：維持比例縮小

```python
import cv2
from lesson05_common import make_demo, new_run, save_png

run = new_run("resize")
image = make_demo()
h, w = image.shape[:2]
new_w = 200
new_h = max(1, round(h * new_w / w))
resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
save_png(run / "resized.png", resized)
print("原始：", image.shape, "縮小：", resized.shape)
print(run)
```

結果是 `(120, 200, 3)`。把原本長方形硬改成正方形會改變物體比例，不只是減少像素。

### 6-2｜最近鄰插值

最近鄰從附近像素取值，適合觀察像素格或保持離散標籤；放大時會出現塊狀邊緣。

### 範例：放大二值圖而不產生灰色

```python
import cv2
import numpy as np
from lesson05_common import new_run, save_png

run = new_run("nearest")
small = np.array([[0, 255], [255, 0]], dtype=np.uint8)
large = cv2.resize(small, (160, 160), interpolation=cv2.INTER_NEAREST)
save_png(run / "nearest.png", large)
print("數值種類：", np.unique(large))
print(run)
```

### 6-3｜雙線性插值

雙線性插值依鄰近像素位置加權，放大後看起來較平滑，但會產生原本沒有的中間數值。

### 範例：放大同一張二值圖

```python
import cv2
import numpy as np
from lesson05_common import new_run, save_png

run = new_run("linear")
small = np.array([[0, 255], [255, 0]], dtype=np.uint8)
large = cv2.resize(small, (160, 160), interpolation=cv2.INTER_LINEAR)
save_png(run / "linear.png", large)
print("是否包含灰色：", bool(np.any((large > 0) & (large < 255))))
print(run)
```

### 6-4｜區域插值

`INTER_AREA` 依來源區域做取樣整合，常用於縮小。細線縮小後可能變淡或消失，不保證能保留所有細節。

### 範例：縮小細線圖

```python
import cv2
import numpy as np
from lesson05_common import new_run, save_png

run = new_run("area")
image = np.full((100, 240), 255, dtype=np.uint8)
image[:, ::4] = 0
small = cv2.resize(image, (60, 25), interpolation=cv2.INTER_AREA)
save_png(run / "original.png", image)
save_png(run / "area.png", small)
print("縮小後數值：", np.unique(small))
print(run)
```

每組四欄中有一欄黑色，縮小後可能成為近似均勻的灰色。請用原始像素倍率查看結果，不要只靠檢視器自動放大後的畫面判斷。

---

## 單元七｜翻轉與補邊

### 7-1｜翻轉

`cv2.flip()` 的 `1` 表示左右翻轉，`0` 表示上下翻轉，`-1` 表示兩個方向都翻轉。翻轉不是一般的傾斜校正。

### 範例：比較翻轉方向

```python
import cv2
from lesson05_common import make_demo, new_run, save_png

run = new_run("flip")
image = make_demo()
for name, mode in [("horizontal", 1), ("vertical", 0), ("both", -1)]:
    save_png(run / f"{name}.png", cv2.flip(image, mode))
print(run)
```

### 7-2｜補上固定背景

`copyMakeBorder()` 的四個厚度依序是上、下、左、右。BGR 白色要用 `(255, 255, 255)`，不能將所有情況都當成單通道影像。

### 範例：增加白色邊界

```python
import cv2
from lesson05_common import make_demo, new_run, save_png

run = new_run("padding")
image = make_demo()
padded = cv2.copyMakeBorder(image, 20, 20, 30, 30,
                            cv2.BORDER_CONSTANT, value=(255, 255, 255))
save_png(run / "padded.png", padded)
print(padded.shape)
print(run)
```

結果是 `(280, 460, 3)`。補邊增加畫布，不會讓原物體變大；縮放會改變物體占用的像素數，兩者不同。

---

## 單元八｜繪圖與遮罩

### 8-1｜線段、矩形與圓

繪圖函式通常會直接修改傳入陣列。用 `image.copy()` 產生標記版，保留原始資料。

### 範例：畫線

```python
import cv2
from lesson05_common import make_demo, new_run, save_png
run = new_run("line")
marked = make_demo().copy()
cv2.line(marked, (20, 140), (380, 140), (0, 0, 255), thickness=2)
save_png(run / "line.png", marked)
print(run)
```

### 範例：畫矩形

```python
import cv2
from lesson05_common import make_demo, new_run, save_png
run = new_run("rectangle")
marked = make_demo().copy()
cv2.rectangle(marked, (25, 25), (135, 125), (0, 0, 0), thickness=2)
save_png(run / "rectangle.png", marked)
print(run)
```

### 範例：畫圓

```python
import cv2
from lesson05_common import make_demo, new_run, save_png
run = new_run("circle")
marked = make_demo().copy()
cv2.circle(marked, (200, 190), 15, (0, 0, 255), thickness=-1)
save_png(run / "circle.png", marked)
print(run)
```

`thickness=-1` 表示填滿矩形或圓形等封閉圖形；正數表示線條粗細。

### 8-2｜文字標記

### 範例：加上英文標籤

```python
import cv2
from lesson05_common import make_demo, new_run, save_png
run = new_run("text")
marked = make_demo().copy()
cv2.putText(marked, "ROI", (30, 145), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 0, 0), 1, cv2.LINE_AA)
save_png(run / "text.png", marked)
print(run)
```

座標通常是文字基線的起點，不是文字框左上角。內建 Hershey 字型不適合直接顯示繁體中文，因此範例使用英文標籤。

### 8-3｜用遮罩保留指定區域

`bitwise_and()` 的 `mask` 是單通道 `uint8` 影像。非零位置允許輸出對應結果，零位置在這個新輸出中保持為零。

### 範例：保留圓形區域

```python
import cv2
import numpy as np
from lesson05_common import make_demo, new_run, save_png

run = new_run("mask")
image = make_demo()
mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.circle(mask, (200, 120), 100, 255, thickness=-1)
selected = cv2.bitwise_and(image, image, mask=mask)
on_white = np.full_like(image, 255)
on_white[mask > 0] = image[mask > 0]
save_png(run / "mask.png", mask)
save_png(run / "on_black.png", selected)
save_png(run / "on_white.png", on_white)
print(run)
```

裁切會改變圖像尺寸；遮罩可以保留原尺寸，只決定哪些位置有內容。遮罩的白色表示「選中」，不代表選中的物體原本就是白色。

---

## 綜合實作｜圖片檢查、ROI 與預覽輸出

### 一、從需求推導步驟

希望取得圖片尺寸，框出中央區域，裁切、等比例縮小，再產生原色與灰階並排的預覽。不要在讀圖之前先假設尺寸，也不要在原圖上畫框後又把框線送進下一個處理步驟。

```text
產生示範圖或讀取指定照片
    ↓
記錄形狀、型別與來源
    ↓
依尺寸決定中央 ROI
    ↓
原圖副本畫框；原始陣列裁切
    ↓
等比例縮小 ROI
    ↓
灰階轉換、通道統一、並排預覽
    ↓
存新目錄與 JSON 紀錄
```

### 二、完整程式

存成 **`lesson05_image_inspector.py`**。這支程式不依賴前面的共用檔案；不指定參數時處理自製色塊，指定圖片路徑時則讀取該圖片。指定路徑讀取失敗會報錯，不會改用示範圖假裝成功。

```python
from pathlib import Path
from tempfile import mkdtemp
import json
import sys
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent


def make_demo():
    image = np.full((240, 400, 3), 245, dtype=np.uint8)
    for x, color in [(30, (255, 0, 0)), (150, (0, 255, 0)), (270, (0, 0, 255))]:
        image[30:120, x:x + 100] = color
    image[160:162, 30:370] = 0
    return image


def read_image(path):
    raw = Path(path).read_bytes()
    if not raw:
        raise ValueError("來源檔案是空的")
    image = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("來源不是可解碼的圖片")
    return image


def write_png(path, image):
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("圖片編碼失敗")
    with Path(path).open("xb") as file:
        file.write(buffer.tobytes())


def main():
    if len(sys.argv) > 1:
        source = Path(sys.argv[1]).expanduser().resolve()
        image = read_image(source)
        source_name = source.name
    else:
        image = make_demo()
        source_name = "generated_demo"

    h, w = image.shape[:2]
    if min(h, w) < 4:
        raise ValueError("圖片太小，無法進行中央裁切")
    x1, y1, x2, y2 = w // 4, h // 4, 3 * w // 4, 3 * h // 4
    crop = image[y1:y2, x1:x2].copy()
    ch, cw = crop.shape[:2]
    scale = min(1.0, 300 / cw)
    resized = cv2.resize(crop, (max(1, round(cw * scale)), max(1, round(ch * scale))),
                         interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    preview = np.concatenate([resized, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)], axis=1)
    marked = image.copy()
    cv2.rectangle(marked, (x1, y1), (x2 - 1, y2 - 1), (0, 0, 255), 2)

    root = BASE_DIR / "output" / "lesson05"
    root.mkdir(parents=True, exist_ok=True)
    run = Path(mkdtemp(prefix="inspect_", dir=str(root)))
    outputs = {"original": image, "marked": marked, "crop": crop,
               "resized": resized, "gray": gray, "preview": preview}
    for name, result in outputs.items():
        write_png(run / f"{name}.png", result)
    info = {
        "source": source_name,
        "source_shape": list(image.shape),
        "dtype": str(image.dtype),
        "roi_xyxy_exclusive": [x1, y1, x2, y2],
        "crop_shape": list(crop.shape),
        "preview_shape": list(preview.shape),
    }
    (run / "info.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(info, ensure_ascii=False, indent=2))
    print("輸出位置：", run)


if __name__ == "__main__":
    main()
```

執行 `python lesson05_image_inspector.py` 可直接看示範；處理照片則執行 `python lesson05_image_inspector.py "照片路徑.png"`。相對輸入路徑以終端機工作目錄為基準，輸出則放在程式旁的 `output/lesson05`。

### 三、核對結果

示範原圖是 `(240, 400, 3)`，中央裁切是 `(120, 200, 3)`，並排預覽是 `(120, 400, 3)`。原圖不應有紅框，只有 `marked.png` 有框線。

`original.png` 是解碼後像素的另存版本，不是來源檔的逐位元組備份。原始照片檔案仍保留在原位置。

### 四、修改練習

把中央裁切改成上半部，先推算新形狀。再加入可設定的 ROI 與縮小上限，檢查空區域、超出邊界與非正數尺寸。最後只在標記圖上加上 ROI 寬高，不要把標記寫進待分析圖片。

---

## 常見問題

**紅藍顛倒：**檢查送給 Matplotlib 的是不是 RGB，送給 OpenCV 編碼的是否維持 BGR。

**`NoneType` 沒有 `shape`：**先檢查讀檔是否成功，不要從裁切參數開始猜。

**裁切結果空白：**確認 `x/y`、起點終點與影像邊界，並檢查 `crop.size`。

**圖片大小不對：**分辨 `shape=(h,w)` 與 `resize(...,(w,h))`。

**存圖失敗或覆寫：**檢查父資料夾、編碼副檔名與開檔模式。不要將輸出路徑設為來源路徑。

## 章末自我檢查

說明檔案位元組如何變成像素。比較灰階與單色通道圖、裁切與遮罩、補邊與縮放。指出哪幾個操作會修改傳入陣列，以及應在哪裡先複製原圖。

## 與後續專題的連結

樂譜照片同樣需要先確認尺寸、方向與內容區域。這些操作本身不會讀出音符，但能建立後續二值化與方向估計需要的影像輸入。

## 延伸閱讀

- [OpenCV 4.8：圖片讀寫定義](https://github.com/opencv/opencv/blob/4.8.0/modules/imgcodecs/include/opencv2/imgcodecs.hpp)
- [OpenCV 4.8：轉換、繪圖與影像處理定義](https://github.com/opencv/opencv/blob/4.8.0/modules/imgproc/include/opencv2/imgproc.hpp)
- [Python 3.11：Path](https://docs.python.org/3.11/library/pathlib.html)

