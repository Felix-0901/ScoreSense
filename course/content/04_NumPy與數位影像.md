# 第 4 章｜NumPy 與數位影像

我們看到的是「一張樂譜」，但電腦看到的是大量數值。

要做影像處理，第一步不是背 OpenCV 函式，而是先知道圖片在程式裡到底長什麼樣子。

## 學習目標

- 理解像素與陣列的關係。
- 使用 NumPy 建立一維、二維與三維陣列。
- 看懂 `shape`、`dtype`、索引與切片。
- 理解灰階圖與彩色圖的資料形狀。
- 用小型陣列模擬裁切與亮度修改。

[TOC]

---

## 單元一｜一張灰階圖可以看成一張數字表

想像只有 4 × 4 像素的小圖：

```python
import numpy as np

image = np.array([
    [255, 255, 255, 255],
    [255,   0,   0, 255],
    [255,   0,   0, 255],
    [255, 255, 255, 255],
], dtype=np.uint8)

print(image)
print(image.shape)
print(image.dtype)
```

如果約定：

```text
0   = 黑
255 = 白
```

中間就會形成黑色方塊。

### 為什麼是 `uint8`？

`uint8` 可以保存 0～255，正好符合常見 8-bit 影像的像素範圍。

---

## 單元二｜shape 告訴我們圖片大小

```python
print(image.shape)
```

結果：

```text
(4, 4)
```

順序是：

```text
(高度, 寬度)
```

不是 `(x, y)`。

這個觀念非常重要，因為 OpenCV 後面很多錯誤都來自把「列、欄」與「x、y」混在一起。

---

## 單元三｜索引與像素位置

```python
print(image[0, 0])
print(image[1, 1])
```

`image[row, column]` 先列再欄。

如果用幾何座標描述某點通常會說 `(x, y)`；但 NumPy 陣列通常寫 `[y, x]`。

```text
幾何座標：(x, y)
NumPy：   image[y, x]
```

---

## 單元四｜切片就是裁切的基礎

```python
crop = image[1:3, 1:3]
print(crop)
```

結果是中間 2 × 2。

這和未來：

```python
crop = photo[y1:y2, x1:x2]
```

裁切樂譜完全同一個概念。

### 練習

建立 6 × 8 的陣列，嘗試：

1. 取出前兩列。
2. 取出第 3～5 欄。
3. 取出中央 2 × 3 區域。

每次操作前先寫出你預期的 `shape`。

---

## 單元五｜彩色圖片多一個通道方向

彩色影像常見形狀：

```text
(height, width, 3)
```

最後的 3 是三個顏色通道。

OpenCV 預設使用：

```text
B G R
```

而不是常聽到的 RGB。

例如：

```python
pixel = np.array([255, 0, 0], dtype=np.uint8)
```

在 OpenCV BGR 中代表藍色，不是紅色。

---

## 單元六｜逐像素運算與溢位

如果：

```python
value = np.array([250], dtype=np.uint8)
```

直接做某些整數運算時，要注意 0～255 的範圍。

影像處理套件通常會幫忙處理飽和或轉型，但學生需要知道：**資料型別不是裝飾，它會影響結果。**

### 安全觀察

```python
arr = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
print(arr)
print(arr.astype(np.float32) / 255.0)
```

---

## 綜合實作｜自己做一張「五線譜概念圖」

```python
import numpy as np

canvas = np.full((120, 400), 255, dtype=np.uint8)

for y in [30, 40, 50, 60, 70]:
    canvas[y:y+1, 20:380] = 0

print("shape:", canvas.shape)
print("最小值:", canvas.min())
print("最大值:", canvas.max())
```

這時還沒有顯示圖片，但資料已經存在。

下一章用 OpenCV 把它存成真正的 PNG。

---

## 章末檢核

1. 灰階影像的 `shape` 通常有幾個維度？
2. 彩色影像為什麼多一個 `3`？
3. NumPy 索引的順序通常是 `[x, y]` 還是 `[y, x]`？
4. 切片終點會不會包含？
5. 為什麼 `dtype` 會影響影像運算？
