# 第 24 章｜前端表單、Fetch 與 OpenSheetMusicDisplay

後端 API 已經完成，但一般使用者不想操作 `/docs` 或命令列。

這一章建立最簡單的網頁：選檔案、選模式、送出、顯示結果。

## 學習目標

- 建立 HTML file input 與 select。
- 使用 JavaScript `FormData`。
- 使用 `fetch()` 呼叫 FastAPI。
- 顯示 API 回傳 JSON。
- 使用 OpenSheetMusicDisplay 將 MusicXML 畫成樂譜。

[TOC]

---

## 單元一｜先做靜態 HTML，不接 API

```html
<form id="form">
  <label>
    樂譜檔案
    <input id="file" type="file" required>
  </label>

  <label>
    標註模式
    <select id="mode">
      <option value="solfege">Do Re Mi</option>
      <option value="numbered">1 2 3</option>
      <option value="zhuyin">注音</option>
    </select>
  </label>

  <button type="submit">開始處理</button>
</form>
```

先確認瀏覽器畫面正常，再寫 JavaScript。

---

## 單元二｜攔截 submit

```javascript
const form = document.querySelector('#form');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  console.log('submit');
});
```

`preventDefault()` 避免瀏覽器使用傳統表單方式整頁跳轉。

---

## 單元三｜FormData

```javascript
const file = document.querySelector('#file').files[0];
const mode = document.querySelector('#mode').value;

const data = new FormData();
data.append('file', file);
data.append('mode', mode);
```

名稱必須和 FastAPI endpoint 的參數對得上。

---

## 單元四｜fetch

```javascript
const res = await fetch('/api/process', {
  method: 'POST',
  body: data,
});

const payload = await res.json();
console.log(payload);
```

先在 DevTools Console 看結果。

如果 `res.ok` 是 false：

```javascript
if (!res.ok) {
  throw new Error(payload.detail || '處理失敗');
}
```

---

## 單元五｜顯示狀態

建立：

```html
<div id="status">尚未開始</div>
```

JavaScript：

```javascript
statusBox.textContent = '處理中…';
```

完成：

```javascript
statusBox.textContent = '完成';
```

錯誤：

```javascript
statusBox.textContent = `錯誤：${err.message}`;
```

這比按了按鈕後畫面完全沒反應好很多。

---

## 單元六｜下載 MusicXML

API 回傳：

```json
{
  "musicxml_url": "/api/files/abc123/annotated_solfege.musicxml"
}
```

HTML：

```html
<a id="download" href="#" download>下載 MusicXML</a>
```

JavaScript：

```javascript
document.querySelector('#download').href = payload.musicxml_url;
```

---

## 單元七｜用 OSMD 顯示樂譜

HTML 載入 OpenSheetMusicDisplay：

```html
<script src="https://cdn.jsdelivr.net/npm/opensheetmusicdisplay@1.9.7/build/opensheetmusicdisplay.min.js"></script>
```

準備容器：

```html
<div id="score"></div>
```

取得 XML：

```javascript
const xmlRes = await fetch(payload.musicxml_url);
const xml = await xmlRes.text();
```

顯示：

```javascript
const osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(
  document.querySelector('#score'),
  { autoResize: true }
);

await osmd.load(xml);
osmd.render();
```

現在標註會和 MusicXML 一起被排進樂譜。

---

## 單元八｜先功能正確，再做漂亮 CSS

本專題優先順序：

```text
能選檔案
↓
API 成功
↓
錯誤訊息清楚
↓
結果可下載
↓
樂譜可顯示
↓
最後才美化
```

不要在核心還不能跑時花兩堂課調按鈕陰影。

---

## 章末檢核

1. `FormData` 的作用？
2. `fetch()` 在這裡呼叫哪個端點？
3. `res.ok` 為什麼要檢查？
4. OSMD 是做辨識還是做顯示？
5. 為什麼前端不自己重新分析 MusicXML 音高？
