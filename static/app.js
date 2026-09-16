const form = document.querySelector('#form');
const statusBox = document.querySelector('#status');
const resultBox = document.querySelector('#result');
const submitButton = document.querySelector('#submit');
let osmd = null;

async function health() {
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    statusBox.textContent = data.oemer_available
      ? '環境正常：圖片辨識與 MusicXML 標註皆可使用。'
      : '核心環境正常；目前未偵測到 oemer。你仍可上傳 MusicXML 測試標註。';
  } catch (_) {
    statusBox.textContent = '無法讀取環境狀態。';
  }
}

function formBool(formData, name, checked) {
  formData.append(name, checked ? 'true' : 'false');
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const file = document.querySelector('#file').files[0];
  if (!file) return;

  submitButton.disabled = true;
  resultBox.classList.add('hidden');
  statusBox.textContent = '處理中… 圖片輸入若啟用 OMR，可能需要較長時間。';

  const data = new FormData();
  data.append('file', file);
  data.append('mode', document.querySelector('#mode').value);
  formBool(data, 'preprocess', document.querySelector('#preprocess').checked);
  formBool(data, 'show_accidental', document.querySelector('#showAccidental').checked);
  formBool(data, 'show_octave', document.querySelector('#showOctave').checked);

  try {
    const res = await fetch('/api/process', { method: 'POST', body: data });
    const payload = await res.json();
    if (!res.ok) throw new Error(payload.detail || '處理失敗');

    statusBox.textContent = '完成。';
    resultBox.classList.remove('hidden');
    document.querySelector('#summary').textContent = `辨識／標註 ${payload.notes_count} 個音符；模式：${payload.mode}`;
    document.querySelector('#download').href = payload.musicxml_url;
    document.querySelector('#notes').textContent = JSON.stringify(payload.notes_preview, null, 2);

    const xmlRes = await fetch(payload.musicxml_url);
    const xml = await xmlRes.text();
    const score = document.querySelector('#score');
    score.innerHTML = '';

    if (window.opensheetmusicdisplay) {
      osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(score, {
        autoResize: true,
        drawTitle: true,
      });
      await osmd.load(xml);
      osmd.render();
    } else {
      score.textContent = 'OpenSheetMusicDisplay 載入失敗；你仍可下載產生的 MusicXML。';
    }
  } catch (err) {
    statusBox.textContent = `錯誤：${err.message}`;
  } finally {
    submitButton.disabled = false;
  }
});

health();
