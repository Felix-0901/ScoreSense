# 第 21 章｜CLI、argparse 與使用者參數

目前要改模式可能還要直接改程式碼。真正工具應該讓使用者從命令列選擇功能。

這一章建立 CLI，之後 Web 介面其實只是另一種「把使用者參數送進同一套核心」。

## 學習目標

- 理解 command line interface。
- 使用 `argparse` 建立 subcommand。
- 建立 `process`、`preprocess`、`web` 指令。
- 將 CLI 參數轉成 `process_file()` 參數。
- 統一處理錯誤與 return code。

[TOC]

---

## 一、我們希望怎麼使用？

```bash
python main.py process materials/twinkle.musicxml --mode zhuyin
```

或：

```bash
python main.py preprocess materials/score_skewed.png
```

最後：

```bash
python main.py web
```

同一支 `main.py` 可以有不同工作模式。

---

## 二、最小 argparse

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()

print("Hello", args.name)
```

執行：

```bash
python demo.py Amy
```

---

## 三、subparser

```python
parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)

p_process = sub.add_parser("process")
p_pre = sub.add_parser("preprocess")
```

這就形成：

```text
python main.py process ...
python main.py preprocess ...
```

---

## 四、process 參數

```python
p_process.add_argument("input")
p_process.add_argument(
    "--mode",
    choices=["solfege", "numbered", "zhuyin"],
    default="solfege",
)
p_process.add_argument("--no-preprocess", action="store_true")
p_process.add_argument("--hide-accidental", action="store_true")
p_process.add_argument("--show-octave", action="store_true")
```

使用：

```bash
python main.py process score.jpg --mode numbered --show-octave
```

---

## 五、每個 command 對應函式

```python
def cmd_process(args):
    result = process_file(
        args.input,
        args.mode,
        preprocess=not args.no_preprocess,
        show_accidental=not args.hide_accidental,
        show_octave=args.show_octave,
    )

    print("Job:", result.job_id)
    print("Notes:", len(result.notes))
    print("MusicXML:", result.annotated_musicxml)
    return 0
```

設定：

```python
p_process.set_defaults(func=cmd_process)
```

最後：

```python
return args.func(args)
```

---

## 六、main 的錯誤邊界

```python
def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1
```

這裡是 CLI 最外層，所以可以把未處理錯誤轉成清楚訊息與 exit code。

但 service 內部仍然要保留有意義的錯誤種類。

---

## 練習

1. 加 `--output` 指定輸出檔。
2. 加 `--no-preprocess` 比較辨識結果。
3. 故意輸入不存在檔案，觀察 exit code。
4. 故意輸入 `.pdf`，確認錯誤訊息。

---

## 章末檢核

1. CLI 的價值是什麼？
2. subcommand 解決什麼？
3. `action="store_true"` 的用途？
4. 為什麼 CLI 仍然呼叫同一個 `process_file()`？
5. return code 0 與 1 通常代表什麼？
