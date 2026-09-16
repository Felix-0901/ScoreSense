# 樂譜辨識與自動標註系統 — MVP

這是一份可直接執行、方便繼續教學與擴充的專案骨架。

## 已完成

- PNG/JPG 等樂譜圖片前處理：灰階、對比增強、傾斜估計、二值化預覽
- oemer CLI 介接：圖片 -> MusicXML（選配）
- MusicXML / MXL 讀取
- 音高擷取
- 固定唱名 Do/Re/Mi、數字簡譜 1~7、注音唱名轉換
- 升降記號與簡單八度提示
- 將標註寫回 MusicXML 的獨立 lyric line（不覆蓋原歌詞）
- FastAPI 本機 API
- 簡單網頁：上傳、模式選擇、處理、OSMD 樂譜顯示、下載 MusicXML
- CLI 模式
- 單元測試

## 建議環境

Python 3.11。

核心功能與 OMR 被刻意拆開：即使 oemer 暫時沒裝好，仍可用 `samples/twinkle.musicxml` 測試完整標註流程。

## 快速啟動

```bash
python3.11 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python doctor.py
python main.py web
```

瀏覽器開啟 `http://127.0.0.1:8000`。

## 安裝 OMR（選配）

```bash
pip install -r requirements-omr.txt
python doctor.py
```

第一次使用 oemer 時，模型/checkpoint 可能會另外下載，因此需要網路。

## 不裝 OMR 也能測

```bash
python main.py process samples/twinkle.musicxml --mode zhuyin
```

輸出會出現在 `data/outputs/<job_id>/`。

## CLI 範例

```bash
python main.py process samples/twinkle.musicxml --mode solfege
python main.py process samples/twinkle.musicxml --mode numbered
python main.py process samples/twinkle.musicxml --mode zhuyin --show-octave
python main.py preprocess path/to/score.jpg
python main.py process path/to/score.jpg --mode zhuyin
```

## 專案定位

此版本是「可運作的 MVP」，不是最終商用品質的 OMR。實際辨識準確率主要取決於 OMR 後端與輸入樂譜品質。之後可再加入首調唱名、多聲部/和弦標註策略、PDF、多頁樂譜、MuseScore 輸出、Flutter App 等。
