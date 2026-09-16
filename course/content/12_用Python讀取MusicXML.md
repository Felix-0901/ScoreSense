# 第 12 章｜用 Python 讀取 MusicXML

上一章我們用眼睛讀 XML。現在把同樣的事情交給 Python。

這一章只做「讀取與巡覽」，先不轉 Do Re Mi，也不寫回檔案。

## 學習目標

- 使用 `xml.etree.ElementTree` 解析 XML。
- 取得 root、tag、child 與 attribute。
- 走訪所有 `note`。
- 理解 XML namespace 可能造成的 tag 差異。
- 寫出 `_local_name()` 的概念。

[TOC]

---

## 單元一｜第一次 parse

```python
import xml.etree.ElementTree as ET


tree = ET.parse("materials/tiny_score.musicxml")
root = tree.getroot()

print("root tag:", root.tag)
```

如果看到：

```text
score-partwise
```

或帶有 `{網址}` 的名稱，都可能是正常的。

---

## 單元二｜看第一層孩子

```python
for child in root:
    print(child.tag, child.attrib)
```

`attrib` 是 XML 屬性字典。

例如：

```xml
<part id="P1">
```

會有：

```python
{"id": "P1"}
```

---

## 單元三｜走遍整棵樹

```python
for element in root.iter():
    print(element.tag)
```

這會很多，所以實務上要篩選。

如果沒有 namespace，可以：

```python
for note in root.iter("note"):
    print(note)
```

但不同 MusicXML 來源可能帶 namespace。

---

## 單元四｜namespace 問題

可能遇到：

```text
{http://www.musicxml.org/ns/musicxml}note
```

人眼知道它仍然是 `note`，但字串比較會不同。

我們可以只取得 `}` 後面的名字：

```python
def local_name(tag):
    return tag.split("}", 1)[-1]
```

測試：

```python
print(local_name("note"))
print(local_name("{abc}note"))
```

兩個都得到：

```text
note
```

---

## 單元五｜建立通用走訪函式

```python
def iter_by_local_name(root, name):
    for element in root.iter():
        if local_name(element.tag) == name:
            yield element
```

使用：

```python
for note in iter_by_local_name(root, "note"):
    print("找到 note")
```

### `yield` 先怎麼理解？

這裡可以先把它理解成：「每找到一個符合的元素，就交出去一次。」

不必在這章深入 generator 的所有細節。

---

## 單元六｜找直接子元素

一顆 `<note>` 裡可能有很多東西。

我們要找直接的 `<pitch>`：

```python
def child(element, name):
    for item in element:
        if local_name(item.tag) == name:
            return item
    return None
```

使用：

```python
for note in iter_by_local_name(root, "note"):
    pitch = child(note, "pitch")
    print(pitch)
```

現在休止符可能印出 `None`。

---

## 綜合實作｜印出所有 step

```python
for note in iter_by_local_name(root, "note"):
    pitch = child(note, "pitch")

    if pitch is None:
        print("rest or unpitched note")
        continue

    step_element = child(pitch, "step")

    if step_element is not None:
        print(step_element.text)
```

這是第一次真正讓 Python 從 MusicXML 自己找到音名。

---

## 修改練習

1. 同時印出 octave。
2. 有 alter 才印，沒有時顯示 0。
3. 計算總共有幾顆 pitched note。
4. 計算總共有幾個 rest。

---

## 章末檢核

1. `ET.parse()` 做什麼？
2. root 是什麼？
3. XML attribute 如何取得？
4. namespace 為什麼可能讓 `root.iter("note")` 失效？
5. `child()` 找不到元素時為什麼回傳 `None`？
