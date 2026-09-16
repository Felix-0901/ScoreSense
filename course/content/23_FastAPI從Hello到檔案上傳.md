# 第 23 章｜FastAPI：從 Hello 到檔案上傳

核心功能已經能從 CLI 使用。現在才開始做介面。

FastAPI 的工作不是辨識樂譜，它負責：**接收使用者請求，把資料交給核心程式，再把結果回傳。**

## 學習目標

- 理解前端、後端與 API 的角色。
- 建立第一個 FastAPI app。
- 建立 GET health endpoint。
- 接收 UploadFile 與 Form 參數。
- 呼叫既有 `process_file()`。
- 將不同錯誤轉成 HTTP status code。

[TOC]

---

## 單元一｜先畫出 Web 架構

```text
瀏覽器
↓ HTTP
FastAPI
↓ Python function call
process_file()
↓
Pipeline
↓
結果
↓ JSON
瀏覽器
```

FastAPI 不應該重新實作 converter、OpenCV 或 XML parser。

---

## 單元二｜第一個 API

`app/web.py`：

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/hello")
def hello():
    return {"message": "Hello ScoreSense"}
```

啟動：

```bash
uvicorn app.web:app --reload
```

開啟：

```text
http://127.0.0.1:8000/api/hello
```

應看到 JSON。

---

## 單元三｜health endpoint

```python
from app.services.omr import find_oemer


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "oemer_available": bool(find_oemer()),
        "supported_modes": [
            "solfege",
            "numbered",
            "zhuyin",
        ],
    }
```

這讓前端可以知道環境目前支援到哪裡。

---

## 單元四｜接收上傳檔案

```python
from fastapi import File, UploadFile


@app.post("/api/upload-test")
async def upload_test(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }
```

先只回報資訊，不要一上來就連完整 Pipeline。

---

## 單元五｜把檔案真的存下來

```python
from pathlib import Path
import shutil
import uuid


job_id = uuid.uuid4().hex[:12]
original_name = Path(file.filename or "upload.bin").name
upload_dir = UPLOAD_DIR / job_id
upload_dir.mkdir(parents=True, exist_ok=True)
input_path = upload_dir / original_name

with input_path.open("wb") as out:
    shutil.copyfileobj(file.file, out)
```

為什麼要用：

```python
Path(file.filename).name
```

因為不應該直接信任使用者傳來的完整路徑字串。

---

## 單元六｜Form 參數

```python
from fastapi import Form


mode: str = Form("solfege")
preprocess: bool = Form(True)
show_accidental: bool = Form(True)
show_octave: bool = Form(False)
```

這些之後從 HTML 表單送進來。

---

## 單元七｜呼叫真正核心

```python
result = process_file(
    input_path,
    mode,
    preprocess=preprocess,
    show_accidental=show_accidental,
    show_octave=show_octave,
    job_id=job_id,
)
```

API 只做「接收與轉交」。

---

## 單元八｜HTTP 錯誤

```python
from fastapi import HTTPException

try:
    ...
except OMRUnavailable as exc:
    raise HTTPException(status_code=503, detail=str(exc))
except OMRFailed as exc:
    raise HTTPException(status_code=422, detail=str(exc))
except ValueError as exc:
    raise HTTPException(status_code=400, detail=str(exc))
```

簡化理解：

```text
400 → 使用者輸入有問題
422 → 檔案可以收，但內容處理失敗
503 → 需要的服務／工具目前不可用
500 → 未預期伺服器錯誤
```

---

## 本章實作結果

到本章結束，使用 API 工具或 `/docs` 應該已能：

```text
選一個檔案
↓
POST /api/process
↓
得到 JSON
```

下一章才做真正給一般使用者看的 HTML 畫面。

---

## 章末檢核

1. FastAPI 和 Pipeline 的責任差在哪裡？
2. GET 與 POST 這裡分別拿來做什麼？
3. UploadFile 為什麼要先存到 uploads？
4. 為什麼要建立 health endpoint？
5. HTTP 503 在這個專案可能代表什麼？
