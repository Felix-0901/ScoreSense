# 第 2 章｜Python 基礎語法、資料結構、函式與模組

一支程式通常會經過三個步驟：取得資料、處理資料、產生結果。

例如，成績統計程式需要保存分數、判斷是否及格、重複處理每筆資料，最後算出平均。這些工作分別對應到變數、條件判斷、迴圈、資料結構與函式。

本章從單一數值開始，逐步學會整理多筆資料，再將程式拆成可以重複使用的功能。

## 學習目標

- 正確使用變數、基本型別、運算子、輸入與輸出。
- 使用字串、條件判斷與迴圈處理資料。
- 選擇適合的 `list`、`tuple`、`dict` 與 `set`。
- 分辨賦值、修改物件與複製資料的差異。
- 撰寫具有參數、回傳值與清楚責任的函式。
- 使用模組、主程式入口與基本型別提示。
- 完成可以處理多筆資料的小型程式。

[TOC]

---

## 單元一｜程式的基本寫法

### 1-1｜敘述與執行順序

Python 通常按照程式由上到下的順序執行。使用變數之前，必須先讓它取得一個值。

```python
price = 35
quantity = 3
total = price * quantity

print(total)
```

輸出：

```text
105
```

`total` 保存的是計算當下的結果，不是會持續更新的數學公式。

```python
price = 35
quantity = 3
total = price * quantity

quantity = 5
print(total)

total = price * quantity
print(total)
```

輸出先是 `105`，重新計算之後才是 `175`。

### 1-2｜縮排與區塊

冒號 `:` 後面的縮排表示哪些敘述屬於同一個區塊。本章每一層使用四個空格，不混用 Tab 與空格。

```python
score = 75

if score >= 60:
    print("及格")
    print("已達到標準")

print("檢查結束")
```

前兩個 `print()` 屬於 `if`，最後一個不屬於。將 `score` 改成 `45`，就只會顯示「檢查結束」。

C++ 常用大括號表示區塊，Python 則將縮排視為語法的一部分。一般敘述結尾不需要加分號。

### 1-3｜註解與命名

```python
# 將攝氏溫度轉成華氏溫度
celsius = 25
fahrenheit = celsius * 9 / 5 + 32
print(fahrenheit)
```

`#` 後面到該行結尾的文字是註解，不會當成程式執行。註解適合補充目的或原因，不必把每個符號重新翻譯一次。

變數名稱區分大小寫，`score` 與 `Score` 是不同名稱。名稱不能以數字開頭，也不能使用 `if`、`for`、`class` 等保留字。

使用 `student_name`、`total_score` 這類能說明內容的名稱，比 `a`、`b` 更容易閱讀。也避免把變數命名為 `list`、`str`、`sum` 或 `input`，否則會遮住同名的內建功能。

### 小練習

建立 `lesson02_basics.py`，保存一個商品的單價與數量，計算總價。接著修改數量並重新計算，觀察哪一行讓總價更新。

---

## 單元二｜變數、型別與型別轉換

### 2-1｜常用基本型別

| 型別 | 代表內容 | 範例 |
| --- | --- | --- |
| `int` | 整數 | `12`、`0`、`-5` |
| `float` | 浮點數 | `3.5`、`-0.25` |
| `str` | 字串 | `"Python"`、`"80"` |
| `bool` | 布林值 | `True`、`False` |
| `NoneType` | 沒有值的狀態 | `None` |

```python
age = 16
height = 168.5
name = "小安"
is_ready = True
result = None

print(type(age).__name__)
print(type(height).__name__)
print(type(name).__name__)
print(type(is_ready).__name__)
print(type(result).__name__)
```

輸出依序是 `int`、`float`、`str`、`bool`、`NoneType`。

`type()` 取得物件的型別，這裡的 `.__name__` 取得型別名稱。數字 `80` 可以直接參與加法，字串 `"80"` 則是兩個文字字元，兩者不能混為一談。

`None` 不等於零，也不等於空字串。它常用來表示「尚未取得結果」或「沒有符合的資料」。

### 2-2｜Python 不需要先宣告變數型別

```python
value = 80
print(type(value).__name__)

value = "八十分"
print(type(value).__name__)
```

同一個名稱可以重新指向不同型別的物件，但不代表應該經常改變同一變數的用途。讓名稱與資料意義保持一致，較容易檢查程式。

### 2-3｜明確轉換型別

```python
text = "80"
score = int(text)

print(score + 5)
print(float("3.25"))
print(str(2026) + " 年")
print(int(3.9))
print(int(-3.9))
```

輸出：

```text
85
3.25
2026 年
3
-3
```

`int()` 對浮點數會朝零截去小數部分，不是四捨五入。

`int("3.9")` 會發生 `ValueError`，因為 `"3.9"` 不是整數格式的字串。需要讀取小數時，應使用 `float()`，不能靠隨意轉型掩蓋資料格式的差異。

### 2-4｜布林值與真假判定

零、空字串、空容器與 `None` 在條件判斷中通常視為假。

```python
print(bool(0))
print(bool(""))
print(bool([]))
print(bool(None))
print(bool("False"))
```

最後一行是 `True`：`"False"` 是非空字串，`bool()` 不會把其中的英文解讀成布林值。

需要處理使用者輸入的「是／否」時，應明確比較文字，例如 `answer == "yes"`。

### 2-5｜浮點數的近似值

```python
import math

value = 0.1 + 0.2
print(value)
print(math.isclose(value, 0.3))
```

常見輸出：

```text
0.30000000000000004
True
```

電腦中的浮點數不一定能精確保存每個十進位小數。比較計算結果時，可以依問題需要設定誤差容許值；`math.isclose()` 是判斷兩個數值是否足夠接近的工具。

把數字顯示成兩位小數，不代表內部資料已變成完全精確的小數。

---

## 單元三｜運算子與運算順序

### 3-1｜算術運算

| 運算子 | 用途 | 範例結果 |
| --- | --- | --- |
| `+` | 加法 | `7 + 2` → `9` |
| `-` | 減法 | `7 - 2` → `5` |
| `*` | 乘法 | `7 * 2` → `14` |
| `/` | 一般除法 | `7 / 2` → `3.5` |
| `//` | 向下取整的除法 | `7 // 2` → `3` |
| `%` | 餘數 | `7 % 2` → `1` |
| `**` | 次方 | `2 ** 3` → `8` |

```python
print(8 / 2)
print(-7 // 2)
print(17 % 5)
print(2 ** 4)
```

輸出：

```text
4.0
-4
2
16
```

`/` 即使剛好整除，整數運算的結果仍會是浮點數。`//` 是向負無限大方向取整，因此 `-7 // 2` 不等於 `int(-7 / 2)`。

判斷整數是否為偶數，可以檢查 `number % 2 == 0`。

### 3-2｜賦值與累加

```python
count = 2
count += 3
print(count)

count *= 2
print(count)
```

對這裡的數值而言，`count += 3` 相當於 `count = count + 3`。Python 沒有 C++ 的 `count++` 遞增寫法，請使用 `count += 1`。

### 3-3｜比較運算

```python
score = 75

print(score == 75)
print(score != 60)
print(score > 80)
print(0 <= score <= 100)
```

`=` 是賦值，`==` 是比較。其他常用比較包含 `<`、`<=`、`>`、`>=`。

字串也能比較，但依照字串順序比較，不會自動轉成數字。例如 `"100" < "20"` 是 `True`。要比較分數，應先確認資料是數值。

### 3-4｜邏輯運算與短路

```python
age = 16
has_ticket = True

print(age >= 12 and has_ticket)
print(age < 12 or has_ticket)
print(not has_ticket)
```

`and` 要兩個條件都成立，`or` 只要至少一個成立，`not` 則反轉真假。

當左邊已經能決定結果時，右邊不會執行，稱為「短路」。

```python
count = 0
total = 80

if count > 0 and total / count >= 60:
    print("平均及格")
else:
    print("沒有足夠資料，或平均未達標準")
```

因為 `count > 0` 是假，程式不會執行 `total / count`，因此不會除以零。

Python 的 `and` 與 `or` 實際上會回傳其中一個運算元，不保證回傳 `bool`。寫條件時，讓兩邊都是清楚的比較式最容易理解。

### 3-5｜成員與物件身分

```python
colors = ["red", "green", "blue"]
print("red" in colors)
print("yellow" not in colors)

result = None
print(result is None)
```

`in` 檢查資料是否包含某個項目，`is` 檢查是否為同一個物件。一般數字與字串的內容比較使用 `==`，判斷是否為 `None` 使用 `is None`。

### 3-6｜括號讓意圖清楚

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(-2 ** 2)
print((-2) ** 2)
```

輸出依序是 `14`、`20`、`-4`、`4`。不確定先後順序時，使用括號清楚表達要先算的部分。

### 小練習

將總秒數 `3671` 拆成小時、分鐘與秒。預期結果為 `1` 小時、`1` 分鐘、`11` 秒，試著使用 `//` 與 `%` 完成。

---

## 單元四｜輸入、輸出與格式化

### 4-1｜`print()` 的分隔與結尾

```python
print("Python", "影像處理", "資料分析", sep=" / ")
print("載入", end="...")
print("完成")
```

輸出：

```text
Python / 影像處理 / 資料分析
載入...完成
```

`sep` 決定多個項目之間的分隔文字，`end` 決定輸出結尾。預設分隔是一個空格，結尾是換行。

### 4-2｜`input()` 回傳字串

```python
name = input("請輸入姓名：").strip()
quantity_text = input("請輸入數量：")
quantity = int(quantity_text)

print(f"{name} 購買 {quantity} 份，總價 {quantity * 35} 元")
```

輸入姓名「小安」與數量 `3`，最後會顯示：

```text
小安 購買 3 份，總價 105 元
```

`input()` 等待使用者按 Enter 後回傳文字。上例要求數量必須是可轉成整數的文字；輸入 `abc` 會發生 `ValueError`。第 3 章會學習如何捕捉這類錯誤並提供提示。

### 4-3｜f-string

在字串前加上 `f`，就可以用 `{}` 放入變數或運算結果。

```python
name = "小安"
score = 86.375

print(f"姓名：{name}")
print(f"成績：{score:.2f}")
print(f"編號：{7:03d}")
print(f"及格比例：{3 / 4:.0%}")
```

輸出：

```text
姓名：小安
成績：86.38
編號：007
及格比例：75%
```

`.2f` 顯示兩位小數，`03d` 將整數補成至少三位並在前面補零，`.0%` 以沒有小數位的百分比顯示。

格式化主要改變呈現方式，不會修改原本的 `score`。

---

## 單元五｜字串：文字也是可以處理的資料

### 5-1｜引號、跳脫字元與多行文字

```python
message = "今天學習 Python"
quote = 'He said "Hello".'
lines = "第一行\n第二行"

print(message)
print(quote)
print(lines)
```

單引號與雙引號都能建立字串。`\n` 表示換行、`\t` 表示 Tab、`\\` 表示一個反斜線。

三引號可以保存多行文字；函式開頭的三引號字串也可以作為說明文件。

```python
message = """第一行
第二行
第三行"""
print(message)
```

### 5-2｜索引與切片

```python
word = "Python"

print(word[0])
print(word[-1])
print(word[1:4])
print(word[:3])
print(word[3:])
print(word[::2])
print(word[::-1])
```

輸出：

```text
P
n
yth
Pyt
hon
Pto
nohtyP
```

索引從 `0` 開始，`-1` 表示最後一個項目。切片的形式為 `資料[起點:終點:步長]`，包含起點、不包含終點。

索引超出範圍會發生 `IndexError`；切片的終點超出範圍，則會取到可取得的位置。步長不能是零。

### 5-3｜字串不能原地修改

```python
word = "python"
new_word = "P" + word[1:]

print(word)
print(new_word)
```

輸出是 `python` 與 `Python`。`word[0] = "P"` 不能用來修改字串，因為字串是不可變物件。

### 5-4｜常用方法

```python
text = "  Python,OpenCV,JSON  "
cleaned = text.strip()
items = cleaned.split(",")

print(cleaned)
print(items)
print(" / ".join(items))
print("photo.PNG".lower())
print("hello".upper())
print("a-b-c".replace("-", "/"))
print("photo.png".endswith(".png"))
print("lesson02.py".startswith("lesson"))
```

`.strip()` 移除前後空白，不會刪掉文字中間所有空格。

`.split()` 將字串拆成串列，`.join()` 則將多個字串組合成一個字串。傳給 `.join()` 的項目必須是字串。

```python
numbers = [10, 20, 30]
texts = []

for number in numbers:
    texts.append(str(number))

print(", ".join(texts))
```

輸出：

```text
10, 20, 30
```

這裡先使用串列保存轉換結果，串列的操作會在單元九完整說明。

### 小練習

將 `"  apple, banana,orange  "` 整理成三個沒有前後空白的水果名稱，再組成 `"apple / banana / orange"`。注意：只對整段文字做一次 `.strip()`，不會移除 `banana` 前面的空白。

---

## 單元六｜條件判斷

### 6-1｜`if`、`elif`、`else`

```python
score = 82

if score >= 90:
    level = "優良"
elif score >= 60:
    level = "及格"
else:
    level = "待加強"

print(level)
```

程式由上到下檢查條件，執行第一個成立的分支，其餘分支便不再檢查。

順序會影響結果：如果先寫 `score >= 60`，那麼 `95` 也會先進入這個分支。

### 6-2｜先確認範圍，再判斷內容

```python
score = 105

if not 0 <= score <= 100:
    print("分數應介於 0 到 100")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

資料不合理與資料未達標準是不同情況。`105` 不應直接被當成正常及格分數。

### 6-3｜多個 `if` 與同一串 `elif` 的差異

```python
number = 12

if number % 2 == 0:
    print("可以被 2 整除")

if number % 3 == 0:
    print("可以被 3 整除")
```

兩個條件互相獨立，因此兩行都會顯示。如果改成 `if ... elif ...`，只會選擇其中一個分支。

### 6-4｜條件運算式

```python
score = 75
label = "及格" if score >= 60 else "不及格"
print(label)
```

形式是 `成立時的值 if 條件 else 不成立時的值`。它適合單純選擇一個值；需要執行多個步驟時，仍使用一般 `if` 區塊。

### 小練習

設定三角形的三個邊長。先確認三邊都大於零，再確認任兩邊和大於第三邊，輸出能否構成三角形。

---

## 單元七｜`for` 迴圈與逐筆處理

### 7-1｜直接走訪資料

```python
names = ["小安", "小晴", "小宇"]

for name in names:
    print(f"你好，{name}")
```

`name` 在每一次迴圈取得一個項目。Python 的 `for` 不只是在計數，更常用來走訪字串、串列或其他可以逐項取出的資料。

### 7-2｜`range()`

```python
print(list(range(5)))
print(list(range(2, 6)))
print(list(range(2, 10, 2)))
print(list(range(5, 0, -1)))
```

輸出：

```text
[0, 1, 2, 3, 4]
[2, 3, 4, 5]
[2, 4, 6, 8]
[5, 4, 3, 2, 1]
```

`range()` 的終點不包含在結果中。步長為正時向上走，為負時向下走；方向不符時可能沒有任何項目。

`range()` 本身不是串列。這裡使用 `list()`，是為了將其中的項目列出來觀察。

### 7-3｜累加與計數

```python
scores = [72, 85, 58, 91]
total = 0
passed_count = 0

for score in scores:
    total += score
    if score >= 60:
        passed_count += 1

print("總分：", total)
print("及格人數：", passed_count)
```

輸出總分 `306`、及格人數 `3`。累加變數必須在迴圈之前初始化，不能每次迴圈都重新設成零。

### 7-4｜`enumerate()`：同時取得編號與資料

```python
names = ["小安", "小晴", "小宇"]

for number, name in enumerate(names, start=1):
    print(number, name)
```

輸出：

```text
1 小安
2 小晴
3 小宇
```

這裡使用兩個名稱接住一組資料，稱為「拆包」。`start=1` 只改變編號的起點，不會改變串列索引仍從零開始的規則。

### 7-5｜`zip()`：配對多組資料

```python
names = ["小安", "小晴", "小宇"]
scores = [72, 85, 91]

for name, score in zip(names, scores):
    print(f"{name}：{score}")
```

`zip()` 預設以最短的一組資料為準，多出來的項目不會被處理。當兩組資料必須一一對應時，可以使用 `zip(names, scores, strict=True)`；長度不同時會在走訪過程中發生 `ValueError`。

不要讓姓名與分數在不知情的情況下錯配或遺漏。

---

## 單元八｜`while`、流程控制與巢狀迴圈

### 8-1｜依條件重複執行

```python
count = 3

while count > 0:
    print(count)
    count -= 1

print("開始")
```

`while` 在每次進入區塊前檢查條件。少了 `count -= 1`，條件就會一直成立，形成無窮迴圈。

一般已知要走訪哪些資料時用 `for`；需要持續執行直到條件改變時，可以用 `while`。

### 8-2｜`break`：結束迴圈

```python
numbers = [3, 7, 12, 15]

for number in numbers:
    if number >= 10:
        print("第一個符合條件的數：", number)
        break
```

找到 `12` 後便停止，不會再處理 `15`。`break` 只結束它所在的最內層迴圈。

### 8-3｜`continue`：跳過本次剩餘工作

```python
numbers = [3, -1, 5, -2, 8]
total = 0

for number in numbers:
    if number < 0:
        continue
    total += number

print(total)
```

輸出 `16`。負數會被略過，但整個迴圈仍繼續執行。

### 8-4｜`pass` 不會跳到下一次迴圈

```python
for number in [1, 2]:
    if number == 1:
        pass
    print(number)
```

輸出仍包含 `1` 與 `2`。`pass` 只是「不做任何事情」的合法敘述，不等於 `continue`，也不等於 `break`。

### 8-5｜巢狀迴圈

```python
for row in range(2):
    for column in range(3):
        print(f"({row}, {column})", end=" ")
    print()
```

輸出：

```text
(0, 0) (0, 1) (0, 2) 
(1, 0) (1, 1) (1, 2) 
```

外層每執行一次，內層就完整走完三次。這種結構可以用來走訪表格中的每一列與每一欄。

### 8-6｜迴圈的 `else`

```python
numbers = [3, 5, 7]

for number in numbers:
    if number % 2 == 0:
        print("找到偶數")
        break
else:
    print("沒有找到偶數")
```

這個 `else` 屬於 `for`。當迴圈正常走完、沒有被 `break` 中止時，才會執行；它不是在判斷迴圈中的 `if` 是否為假。

### 小練習

寫一個最多接受三次輸入的猜數字程式，答案固定為 `7`。猜對就 `break`，三次都沒猜對則顯示答案。先假設每次都輸入整數。

---

## 單元九｜List：有順序、可以修改的資料

### 9-1｜建立與讀取

```python
scores = [72, 85, 58, 91]

print(scores[0])
print(scores[-1])
print(scores[1:3])
print(len(scores))
```

輸出依序為 `72`、`91`、`[85, 58]`、`4`。

空串列寫成 `[]`。串列可以保存不同型別，但同一組資料通常維持一致的意義，例如一整串分數。

### 9-2｜新增、修改與刪除

```python
colors = ["red", "blue"]
colors.append("green")
colors.insert(1, "yellow")
colors[0] = "orange"

print(colors)

removed = colors.pop()
colors.remove("yellow")
del colors[0]

print("移除的最後一項：", removed)
print("剩下：", colors)
```

輸出：

```text
['orange', 'yellow', 'blue', 'green']
移除的最後一項： green
剩下： ['blue']
```

`append()` 在最後新增一項；`insert()` 插入指定位置；`pop()` 移除並回傳項目；`remove()` 移除第一個相等的值；`del` 可依索引或切片刪除。

`remove()` 找不到目標會發生 `ValueError`，從空串列 `pop()` 會發生 `IndexError`。

### 9-3｜`append()` 與 `extend()`

```python
first = [1, 2]
first.append([3, 4])

second = [1, 2]
second.extend([3, 4])

print(first)
print(second)
```

輸出：

```text
[1, 2, [3, 4]]
[1, 2, 3, 4]
```

`append()` 把整個物件當成一項，`extend()` 則將可走訪資料中的項目逐個加入。

### 9-4｜排序與反轉

```python
scores = [72, 85, 58, 91]
ordered = sorted(scores)

print(scores)
print(ordered)

scores.sort(reverse=True)
print(scores)

scores.reverse()
print(scores)
```

`sorted()` 產生新的串列，原串列不變；`.sort()` 與 `.reverse()` 則直接修改原串列，而且回傳 `None`。

因此不要寫 `scores = scores.sort()`，否則 `scores` 最後會變成 `None`。

### 9-5｜統計與邊界情況

```python
scores = [72, 85, 58, 91]

if scores:
    print("總分：", sum(scores))
    print("最低：", min(scores))
    print("最高：", max(scores))
    print("平均：", sum(scores) / len(scores))
else:
    print("沒有成績資料")
```

空串列的 `sum()` 是 `0`，但 `min([])`、`max([])` 會發生 `ValueError`，平均也不能除以零。處理空資料是程式本身需要定義的行為。

走訪串列時，不要同時任意刪除其中的項目，否則索引移動可能導致漏處理。要篩選資料時，可以建立新的串列。

---

## 單元十｜Tuple：固定組合與拆包

### 10-1｜建立 tuple

```python
point = (120, 80)
single = (5,)
not_tuple = (5)

print(point[0])
print(type(single).__name__)
print(type(not_tuple).__name__)
```

輸出是 `120`、`tuple`、`int`。單一項目的 tuple 必須有逗號，只有括號不會自動形成 tuple。

Tuple 的項目不能被重新指定，適合表達座標、尺寸等一組具有固定意義的資料。Tuple 不代表內容一定不能包含可變物件；如果裡面放了串列，串列本身仍可修改。

### 10-2｜拆包與交換

```python
point = (120, 80)
x, y = point
print(x, y)

left = 3
right = 8
left, right = right, left
print(left, right)

first, *middle, last = [10, 20, 30, 40]
print(first, middle, last)
```

輸出：

```text
120 80
8 3
10 [20, 30] 40
```

一般拆包要求兩邊項目數量相同，否則會發生 `ValueError`。帶星號的名稱可以接住中間多個項目，得到的是串列。

---

## 單元十一｜Dictionary：用名稱查找資料

### 11-1｜鍵與值

```python
student = {
    "name": "小安",
    "score": 82,
    "passed": True,
}

print(student["name"])
print(student["score"])
```

字典由「鍵 `key` → 值 `value`」組成，查找時用鍵，不是用項目的位置。

鍵必須可以雜湊，常見選擇是字串或整數，不能直接把串列當成鍵。同一個鍵只會有一個對應值；再次指定同名鍵會更新原值。

### 11-2｜讀取、增加與刪除

```python
student = {"name": "小安", "score": 82}
student["score"] = 88
student["class_name"] = "A 班"

print(student.get("nickname", "未設定"))
print("score" in student)

removed = student.pop("class_name")
print(removed)
print(student)
```

`student["missing"]` 會發生 `KeyError`，`.get("missing", 預設值)` 則在鍵不存在時回傳預設值。

`.get()` 不會驗證內容：如果鍵存在但值是 `None`，它仍回傳 `None`，不會改用預設值。

`"score" in student` 檢查的是鍵，不是所有值。

### 11-3｜走訪字典

```python
student = {"name": "小安", "score": 82}

for key in student:
    print("鍵：", key)

for key, value in student.items():
    print(key, "→", value)

print(list(student.keys()))
print(list(student.values()))
```

`.keys()`、`.values()` 與 `.items()` 分別提供鍵、值、鍵值配對的檢視。這些不是獨立複製的串列；需要串列時可明確使用 `list()`。

字典保留插入順序，但不是自動依鍵名排序。即使有順序，`student[0]` 仍表示查找鍵 `0`，不是取第一筆。

### 11-4｜計算出現次數

```python
fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
counts = {}

for fruit in fruits:
    counts[fruit] = counts.get(fruit, 0) + 1

print(counts)
```

輸出：

```text
{'apple': 3, 'banana': 2, 'orange': 1}
```

第一次遇到名稱時，原本次數視為零，再加一；之後則在已有次數上繼續累加。

### 小練習

建立商品名稱與價格的字典。給定一串購物品項，計算總價；遇到不存在的商品時顯示名稱，而不是讓整段程式直接停止。

---

## 單元十二｜Set：去除重複與集合運算

```python
first = {"apple", "banana", "orange"}
second = {"banana", "grape"}

print(sorted(first | second))
print(sorted(first & second))
print(sorted(first - second))
print(sorted(first ^ second))
```

`|` 是聯集、`&` 是交集、`-` 是差集、`^` 是對稱差集，也就是只出現在其中一邊的項目。

集合不保存重複項目，也不能用索引取第幾項。不要依賴集合的走訪順序；上例用 `sorted()`，讓輸出容易比較。

```python
numbers = [3, 1, 3, 2, 1]
unique = set(numbers)
unique.add(5)
unique.discard(9)

print(sorted(unique))
print(type({}).__name__)
print(type(set()).__name__)
```

空集合必須使用 `set()`，`{}` 是空字典。`.discard()` 在項目不存在時不報錯；`.remove()` 則會發生 `KeyError`。

### 四種容器如何選擇？

| 型別 | 主要用途 | 讀取方式 | 能否修改容器內容 |
| --- | --- | --- | --- |
| `list` | 有順序、可能增減的多筆資料 | 索引 | 可以 |
| `tuple` | 座標等固定組合 | 索引或拆包 | 不能重新指定項目 |
| `dict` | 依名稱查找的對應關係 | 鍵 | 可以 |
| `set` | 去重、成員檢查、集合運算 | 成員檢查，沒有索引 | 可以 |

---

## 單元十三｜巢狀資料、賦值與複製

### 13-1｜串列裡放字典

```python
students = [
    {"name": "小安", "score": 82},
    {"name": "小晴", "score": 91},
    {"name": "小宇", "score": 58},
]

print(students[0]["name"])

for student in students:
    print(f"{student['name']}：{student['score']}")
```

最外層的串列保存多筆資料，每筆字典則保存同一個人的不同欄位。這比把姓名、分數分開放進兩個串列更容易維持對應關係。

### 13-2｜二維串列

```python
grid = [
    [10, 20, 30],
    [40, 50, 60],
]

print(grid[1][2])

for row in grid:
    print(sum(row))
```

`grid[1][2]` 先取第 2 列，再取其中第 3 個項目，結果為 `60`。

### 13-3｜賦值不等於複製

```python
original = [10, 20]
alias = original
alias.append(30)

print(original)
print(alias is original)
```

`original` 也會變成 `[10, 20, 30]`，因為兩個名稱指向同一個串列。

```python
original = [10, 20]
copied = original.copy()
copied.append(30)

print(original)
print(copied)
print(copied is original)
```

這次原串列不變，因為 `.copy()` 建立新的外層串列。

### 13-4｜淺複製與深複製

```python
import copy

original = [[10, 20], [30, 40]]
shallow = original.copy()
deep = copy.deepcopy(original)

shallow[0][0] = 99

print(original)
print(deep)
```

輸出：

```text
[[99, 20], [30, 40]]
[[10, 20], [30, 40]]
```

淺複製只建立新的外層容器，內層串列仍共用。`deepcopy()` 在這個例子中也複製了內層資料。

建立多列資料時，同樣要避免不小心共用內層串列：`[[0] * 3] * 2` 會讓兩列指向同一個串列。需要獨立的兩列時，可寫成 `[[0] * 3 for _ in range(2)]`；下一單元會介紹這種推導式。

---

## 單元十四｜推導式、排序與常用內建工具

### 14-1｜串列推導式

先看一般迴圈：

```python
squares = []
for number in range(1, 5):
    squares.append(number ** 2)
print(squares)
```

也可以寫成：

```python
squares = [number ** 2 for number in range(1, 5)]
print(squares)
```

兩者都得到 `[1, 4, 9, 16]`。推導式適合「逐項轉換，形成新資料」的短小工作。

### 14-2｜加入篩選條件

```python
scores = [72, 85, 58, 91]
passed = [score for score in scores if score >= 60]
labels = ["及格" if score >= 60 else "不及格" for score in scores]

print(passed)
print(labels)
```

第一行推導式會減少項目，只留下及格分數；第二行則為每筆資料產生標籤，項目數量不變。

字典也有推導式：

```python
prices = {"apple": 30, "banana": 20}
discounted = {name: price * 0.9 for name, price in prices.items()}
print(discounted)
```

如果一行出現很多巢狀迴圈與條件，改回一般迴圈通常更容易閱讀。

### 14-3｜依指定欄位排序

```python
students = [
    {"name": "小安", "score": 82},
    {"name": "小晴", "score": 91},
    {"name": "小宇", "score": 58},
]

ordered = sorted(students, key=lambda student: student["score"], reverse=True)
print([student["name"] for student in ordered])
```

輸出 `['小晴', '小安', '小宇']`。

`key` 提供取得排序依據的函式。`lambda student: student["score"]` 是一個簡短的匿名函式，收到一筆資料後回傳分數。邏輯較長時，使用下一單元的 `def` 定義一般函式。

### 14-4｜`any()` 與 `all()`

```python
scores = [72, 85, 58, 91]

print(any([score < 60 for score in scores]))
print(all([0 <= score <= 100 for score in scores]))
print(any([]))
print(all([]))
```

輸出依序為 `True`、`True`、`False`、`True`。

`any()` 判斷是否至少有一個項目為真；`all()` 判斷是否全部為真。特別注意 `all([])` 是 `True`，因此「每筆都符合」不代表「至少有一筆資料」。

---

## 單元十五｜函式、參數與回傳值

### 15-1｜定義與呼叫

```python
def rectangle_area(width, height):
    area = width * height
    return area


result = rectangle_area(8, 5)
print(result)
```

輸出 `40`。

`def` 定義函式，`width` 與 `height` 是參數；呼叫時的 `8` 與 `5` 是傳入的引數。函式定義完成時不會立刻計算面積，要呼叫才會執行函式本體。

### 15-2｜`print()` 與 `return`

```python
def show_total(a, b):
    print(a + b)


def calculate_total(a, b):
    return a + b


first = show_total(3, 5)
second = calculate_total(3, 5)

print("first：", first)
print("second：", second)
```

輸出：

```text
8
first： None
second： 8
```

`print()` 負責顯示，`return` 將資料交回呼叫端。沒有明確 `return` 的函式會回傳 `None`。

只負責顯示的函式沒有錯；但後續還要用結果計算時，應回傳資料，而不是只把它印出來。

### 15-3｜提早回傳

```python
def average(numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


print(average([70, 80, 90]))
print(average([]))
```

輸出 `80.0` 與 `None`。執行到 `return` 時，當次函式呼叫就結束，後面的敘述不再執行。

這個函式將「沒有平均值」定義為 `None`，呼叫端必須處理這個情況。不要用零取代沒有資料，因為零也可能是真正的平均分數。

### 15-4｜位置引數、關鍵字引數與預設值

```python
def greet(name, prefix="你好"):
    return f"{prefix}，{name}"


print(greet("小安"))
print(greet("小晴", "早安"))
print(greet(prefix="午安", name="小宇"))
```

一般呼叫中，位置引數必須放在關鍵字引數之前，同一個參數也不能重複傳入。定義一般參數時，沒有預設值的參數應放在有預設值的參數之前。

### 15-5｜回傳多個結果

```python
def bounds(numbers):
    return min(numbers), max(numbers)


lowest, highest = bounds([72, 85, 58, 91])
print(lowest, highest)
```

函式實際回傳一個 tuple，再由兩個變數拆包。這個範例要求輸入非空資料；傳入空串列時，`min()` 與 `max()` 仍會報錯。

### 小練習

撰寫 `is_even(number)`，回傳整數是否為偶數。接著利用這個函式，從一串整數中找出所有偶數。函式內不要只印出答案。

---

## 單元十六｜作用域、可變參數與型別提示

### 16-1｜區域變數與外部變數

```python
name = "外部"


def show_name():
    name = "內部"
    print(name)


show_name()
print(name)
```

輸出先是「內部」，再是「外部」。函式內賦值的 `name` 是區域變數，不會自動改變外面的同名變數。

函式可以讀取適用作用域中的外部名稱，但需要修改資料時，優先透過參數與回傳值表達，避免讓呼叫端猜測哪些全域狀態會被改動。`global` 可以宣告使用模組層級名稱，但不是傳遞資料的必要手段。

### 16-2｜傳入可變物件

```python
def add_item(items, item):
    items.append(item)


values = [10, 20]
add_item(values, 30)
print(values)
```

輸出是 `[10, 20, 30]`。函式內的參數與外部名稱指向同一個串列，修改內容會被外面看見。

重新賦值與修改內容不同：如果函式裡改寫成 `items = [99]`，只是讓區域名稱指向新串列，不會將外面的 `values` 改成 `[99]`。

### 16-3｜不要共用可變的預設值

下面是容易造成意外結果的寫法：

```python
def collect(item, items=[]):
    items.append(item)
    return items


print(collect("apple"))
print(collect("banana"))
```

第二次輸出會是 `['apple', 'banana']`，因為預設的空串列在函式定義時建立，不會在每次呼叫時重新建立。

改用 `None` 表示「沒有傳入容器」：

```python
def collect(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


print(collect("apple"))
print(collect("banana"))
```

這次兩次呼叫會得到各自獨立的串列。

### 16-4｜型別提示與說明字串

```python
def average(numbers: list[float]) -> float | None:
    """計算平均值；空串列回傳 None。"""
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


print(average([70.0, 80.0, 90.0]))
print(average.__doc__)
```

`list[float]` 表示預期收到浮點數串列，`float | None` 表示可能回傳浮點數，也可能沒有結果。型別提示方便閱讀與檢查工具使用，不會自動將錯誤輸入轉型，也不會在執行時強制驗證所有資料。

三引號中的說明字串稱為 docstring，可以用 `help(average)` 查看。

### 16-5｜延伸：`*args`、`**kwargs` 與拆包傳參數

```python
def add_all(*numbers):
    return sum(numbers)


def make_profile(**fields):
    return fields


print(add_all(10, 20, 30))
print(make_profile(name="小安", score=82))
```

`*numbers` 接住多個位置引數，得到 tuple；`**fields` 接住多個關鍵字引數，得到字典。名稱不一定要叫 `args` 或 `kwargs`，星號才是語法的一部分。

呼叫端的星號則用來把容器拆開傳入：

```python
def rectangle_area(width, height):
    return width * height


size = (8, 5)
options = {"width": 8, "height": 5}

print(rectangle_area(*size))
print(rectangle_area(**options))
```

兩次都輸出 `40`。字典的鍵必須對應參數名稱，不能傳入不存在的名稱或重複指定同一參數。

需要讓某個選項只能以名稱傳入時，可以使用單獨的 `*`：

```python
def format_score(score, *, digits=1):
    return f"{score:.{digits}f}"


print(format_score(86.375, digits=2))
```

`digits` 是僅限關鍵字的參數，因此不能用 `format_score(86.375, 2)` 呼叫。

---

## 單元十七｜模組、`import` 與主程式入口

### 17-1｜使用標準函式庫

```python
import math
from statistics import mean

print(math.sqrt(81))
print(mean([70, 80, 90]))
```

`import math` 載入模組，使用時寫 `math.sqrt()`；`from statistics import mean` 則將 `mean` 這個名稱匯入目前的程式。

`import math as m` 可以取別名，之後使用 `m.sqrt()`。不建議使用 `from math import *`，因為很難看出名稱來自哪個模組，也可能與自己的名稱衝突。

本章使用的 `math`、`statistics`、`copy` 等都屬於 Python 標準函式庫。

### 17-2｜建立自己的模組

將下面兩個檔案放在同一個資料夾：

```text
scoresense_course/
├── grade_tools.py
└── lesson02_use_module.py
```

**檔案：`grade_tools.py`**

```python
PASS_SCORE = 60


def is_passed(score):
    return score >= PASS_SCORE


def average(scores):
    if not scores:
        return None
    return sum(scores) / len(scores)
```

**檔案：`lesson02_use_module.py`**

```python
from grade_tools import average, is_passed

scores = [72, 85, 58, 91]

for score in scores:
    print(score, is_passed(score))

print("平均：", average(scores))
```

在這兩個檔案所在的資料夾執行 `python lesson02_use_module.py`。匯入時不寫 `.py` 副檔名。

不要把自己的檔案命名成 `json.py`、`math.py` 等標準模組名稱，避免匯入時誤讀到自己的檔案。

### 17-3｜為什麼需要 `if __name__ == "__main__"`？

模組第一次被匯入時，最外層的敘述會被執行。如果把互動輸入直接寫在最外層，其他程式一匯入它，就可能突然要求使用者輸入。

建立 **`lesson02_entry.py`**：

```python
def greet(name):
    return f"你好，{name}"


def main():
    print(greet("小安"))


if __name__ == "__main__":
    main()
```

直接執行 `python lesson02_entry.py` 時，`__name__` 是 `"__main__"`，因此會呼叫 `main()`。

其他檔案寫 `from lesson02_entry import greet` 時，`__name__` 是模組名稱，便不會執行入口中的 `main()`；函式仍可以正常使用。

### 17-4｜套件與模組的基本差異

模組常是一個 `.py` 檔案；一般 Python 套件則可以用資料夾整理多個模組，並放入 `__init__.py`。例如 `tools/grade.py` 可以透過 `from tools.grade import average` 使用其中的函式。

`__init__.py` 不是主程式入口。一般小練習先將檔案放在同一資料夾即可，不需要為了使用一個函式就建立多層結構。

### 小練習

在 `grade_tools.py` 新增 `highest_score(scores)`，空資料時回傳 `None`。由另一個檔案匯入並測試非空與空串列兩種情況。

---

## 單元十八｜延伸：物件、屬性與方法

字串的 `.strip()`、串列的 `.append()`，都是透過物件呼叫方法。點號後面不一定都是函式：有些名稱代表資料屬性，有些代表可以呼叫的方法。

使用 `class` 可以定義自己的物件型別。

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_passed(self):
        return self.score >= 60


student = Student("小安", 82)
print(student.name)
print(student.score)
print(student.is_passed())
```

`Student` 是類別，`student` 是建立出來的實例。`__init__()` 用來初始化實例資料；`self` 代表目前操作的實例。

`student.name` 讀取屬性，`student.is_passed()` 呼叫方法。呼叫實例方法時，Python 會自動將實例傳給第一個參數，所以不用再手動傳入 `student`。

字典適合直接整理欄位；類別可以將相關資料與行為放在一起。不必把每一組資料都改成類別。

---

## 單元十九｜延伸：`match` 與固定選項

當同一個值需要對應多種固定情況時，可以使用 `match`。它在 Python 3.10 起提供，本課程使用的 Python 3.11 可以使用。

```python
command = "list"

match command:
    case "list":
        print("列出資料")
    case "add":
        print("新增資料")
    case "quit" | "exit":
        print("結束")
    case _:
        print("未知指令")
```

只會執行第一個符合的分支，不需要加 `break`。`_` 表示其他未匹配的情況，`|` 可以在這裡表示多個候選模式。

比對固定字串時要保留引號。`case "list":` 是比對文字，`case name:` 通常是把值綁定到名稱，不是拿它與外部的同名變數比較。

`match` 還能處理資料結構模式；一般分數範圍判斷仍以 `if / elif / else` 較直觀。

---

## 綜合實作｜成績摘要程式

這個程式把多筆資料、篩選、排序、函式與主程式入口組合起來。

輸入資料先限定為格式正確的字典串列，每筆都有姓名，以及介於 `0` 到 `100` 的數值分數。讀取外部檔案與驗證資料會在第 3 章接續完成。

建立 **`lesson02_summary.py`**：

```python
def summarize(students):
    if not students:
        return None

    scores = [student["score"] for student in students]
    passed_names = [
        student["name"]
        for student in students
        if student["score"] >= 60
    ]
    ordered = sorted(
        students,
        key=lambda student: student["score"],
        reverse=True,
    )

    return {
        "count": len(students),
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "passed_names": passed_names,
        "ordered": ordered,
    }


def main():
    students = [
        {"name": "小安", "score": 82},
        {"name": "小晴", "score": 91},
        {"name": "小宇", "score": 58},
        {"name": "小庭", "score": 69},
    ]

    summary = summarize(students)
    if summary is None:
        print("沒有成績資料")
        return

    print(f"人數：{summary['count']}")
    print(f"平均：{summary['average']:.2f}")
    print(f"最高：{summary['highest']}")
    print(f"最低：{summary['lowest']}")
    print("及格：" + "、".join(summary["passed_names"]))
    print("由高到低：")

    for number, student in enumerate(summary["ordered"], start=1):
        print(f"{number}. {student['name']}：{student['score']}")


if __name__ == "__main__":
    main()
```

預期輸出：

```text
人數：4
平均：75.00
最高：91
最低：58
及格：小安、小晴、小庭
由高到低：
1. 小晴：91
2. 小安：82
3. 小庭：69
4. 小宇：58
```

### 修改練習

1. 新增一筆成績，確認人數、平均與排序都會更新。
2. 將資料改成空串列，確認不會除以零。
3. 增加「未及格姓名」與「及格比例」。
4. 將及格門檻改為函式參數，預設為 `60`。
5. 將 `summarize()` 移到另一個模組，由主程式匯入使用。

### 結果檢查

除了觀察畫面，也可以用 `assert` 檢查程式結果。將下列程式另外存成同一資料夾的 **`lesson02_check.py`**：

```python
from lesson02_summary import summarize

result = summarize([
    {"name": "甲", "score": 60},
    {"name": "乙", "score": 80},
])

assert result is not None
assert result["count"] == 2
assert result["average"] == 70.0
assert result["passed_names"] == ["甲", "乙"]
assert summarize([]) is None

print("檢查通過")
```

`assert` 的條件不成立時會發生 `AssertionError`。它適合這類開發期間的結果檢查，但不能取代正式輸入驗證，因為以最佳化模式執行 Python 時可能停用斷言。

---

## 常見錯誤整理

| 現象 | 常見原因 | 檢查方向 |
| --- | --- | --- |
| `NameError` | 名稱尚未定義、大小寫不一致 | 查看名稱第一次賦值的位置 |
| `TypeError` | 不相容的型別、引數使用錯誤 | 用 `type()` 查看實際資料 |
| `ValueError` | 型別可以接受，但內容不符合要求 | 檢查數字文字、拆包數量等 |
| `IndexError` | 索引超出範圍 | 檢查 `len()` 與索引起點 |
| `KeyError` | 字典沒有這個鍵 | 檢查鍵名、`in` 或適合的預設值 |
| 變數突然變成 `None` | 接住只修改原物件的方法結果 | 區分 `.sort()` 與 `sorted()` |
| 原始資料跟著改變 | 兩個名稱或巢狀資料共用物件 | 檢查賦值、淺複製與深複製 |
| 迴圈一直執行 | 停止條件永遠不變 | 檢查條件與更新位置 |

---

## 章末自我檢查

1. `80`、`80.0` 與 `"80"` 的型別有什麼不同？
2. `=`、`==`、`is` 分別處理什麼問題？
3. `/` 與 `//` 有什麼差異？負數時會怎樣？
4. 為什麼 `input()` 的結果不能直接當成整數？
5. `word[1:4]` 包含哪些索引？
6. 多個獨立的 `if` 與一串 `if / elif` 有何差異？
7. `break`、`continue` 與 `pass` 分別做什麼？
8. `append()` 與 `extend()` 有何差異？
9. 要保存一組座標、學生資料、去重後標籤，各適合哪種容器？
10. 為什麼 `copied = original` 不會複製串列？
11. `.get()` 能不能保證字典的值符合需求？
12. `print()` 與 `return` 的用途有什麼不同？
13. 可變物件作為預設參數，為什麼可能共用資料？
14. 型別提示會不會自動驗證或轉換輸入？
15. 匯入模組時，主程式入口判斷有什麼作用？

---

## 與後續專題的連結

圖片尺寸可以用一組數值表示，辨識結果可以保存成字典串列，重複轉換則可以包成函式。

這些應用的資料不同，但仍建立在本章的索引、迴圈、容器、函式與模組之上。下一章會讓資料不再只存在程式內，而是能從檔案讀入並保存結果。

## 延伸閱讀

- [Python 3.11：基本語法與資料](https://docs.python.org/3.11/tutorial/introduction.html)
- [Python 3.11：流程控制與函式](https://docs.python.org/3.11/tutorial/controlflow.html)
- [Python 3.11：資料結構](https://docs.python.org/3.11/tutorial/datastructures.html)
- [Python 3.11：模組](https://docs.python.org/3.11/tutorial/modules.html)
- [Python 3.11：類別](https://docs.python.org/3.11/tutorial/classes.html)
- [Python 3.11：內建函式](https://docs.python.org/3.11/library/functions.html)
- [Python 3.11：內建型別](https://docs.python.org/3.11/library/stdtypes.html)
