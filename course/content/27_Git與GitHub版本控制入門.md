# 第 27 章｜Git 與 GitHub：從版本控制到專案協作

完成 ScoreSense 後，你可能會開始修改功能、修正 Bug，甚至與同學共同開發。這時會遇到一個問題：

**「昨天的程式還能用，今天改完壞掉了；我怎麼知道改了什麼？又要怎麼把成果交給別人？」**

這章從零認識 Git 與 GitHub。你不必先有 Git 經驗，也不需要付費帳號。範例主要以 Windows 為主，另外提供 macOS 與 Linux 指令。**請在全新的練習資料夾操作，不要對正式的 ScoreSense 專案直接實驗還原或合併。**

## 學習目標

- 知道 Git、GitHub、Repository、Commit、Branch、Remote 的角色。
- 在 Windows／macOS／Linux 安裝並確認 Git。
- 建立 GitHub 帳號，設定 Git 作者資訊，使用 HTTPS 或 SSH 驗證。
- 操作 add、commit、push、clone、pull、fetch、log、diff 與分支。
- 了解 Pull Request、版本還原、合併衝突與 .gitignore。
- 能用 VS Code 圖形化介面操作 Git，並知道如何查閱問題。

[TOC]

---

## 單元一｜Git 與 GitHub 是什麼？為什麼要學版本控制？

### 1-1 先想像沒有 Git 的情況

假設你做了一個 Python 專題，資料夾變成：

~~~text
project/
├── main_最初版.py
├── main_修改版.py
├── main_最後版.py
└── main_真的最後版2.py
~~~

這樣很難知道哪份是正確版本，也無法清楚比較每次改動。

**Git（分散式版本控制系統）**會在同一份專案內保留一連串修改紀錄，讓我們能查看「誰在什麼時候修改了哪些內容」。每筆正式記錄叫作 **Commit（提交）**。

**GitHub（程式碼託管與協作平台）**則讓 Git 專案可以存放在網路上、分享給同學、提出修改建議並審查程式。**Git 不等於 GitHub：離線也能使用 Git。**

### 1-2 六個必懂名詞

| 英文 | 中文 | 可以怎麼理解 |
| --- | --- | --- |
| Repository / Repo | 版本庫／儲存庫 | 被 Git 管理的一個專案 |
| Working directory | 工作目錄 | 電腦上正在編輯的檔案 |
| Staging area / Index | 暫存區 | 選出「下一筆 Commit 要包含」的修改 |
| Commit | 提交紀錄 | 一份有說明的版本快照 |
| Branch | 分支 | 獨立發展的一條修改路線 |
| Remote / origin | 遠端版本庫／遠端名稱 | 例如 GitHub 上對應的 Repo；origin 只是慣用別名 |

### 1-3 一張圖理解 Git 工作流程

~~~text
本機（你的電腦）                                  遠端（GitHub）
┌──────────────────────────────────┐          ┌──────────────────┐
│ 工作目錄 --git add--> 暫存區      │          │ 遠端 Repository  │
│                      │           │          │                  │
│                 git commit       │          │                  │
│                      ↓           │          │                  │
│                 本機 Repository --git push-->│                  │
│                      ↑           │          │                  │
│                 git pull / fetch <-----------│                  │
└──────────────────────────────────┘          └──────────────────┘
~~~

- 修改檔案，不代表已建立版本紀錄。
- <code>git add</code> 是選取要提交的修改；<code>git commit</code> 才是建立本機版本。
- <code>git push</code> 會把已提交的版本送到遠端；單純 Commit 不會自動上傳。
- <code>git pull</code> 會取得遠端更新並嘗試整合；<code>git fetch</code> 只先取得遠端資料。

### 想一想

1. 沒有網路時可以使用 <code>git commit</code> 嗎？（可以，因為 Commit 在本機。）
2. 只有在 GitHub 網站新增 Repo，自己的電腦會自動出現專案檔案嗎？（不會。）
3. 你修改了程式卻忘了 Commit，GitHub 能直接看到這些修改嗎？（不能。）

---

## 單元二｜安裝 Git 與確認環境

### 2-1 Windows（建議優先照這一段）

1. 開啟 [Git 官方 Windows 安裝頁](https://git-scm.com/install/windows)。
2. 下載符合電腦架構的安裝程式（一般 Windows 電腦通常是 x64；ARM 裝置選 ARM64）。
3. 執行安裝程式。第一次學習可以先使用預設選項；有疑問時先記下畫面，不要隨意修改不理解的進階設定。
4. 安裝完成後，從開始選單開啟 **Git Bash**，或重新啟動 VS Code 的終端機。
5. 輸入：

~~~bash
git --version
~~~

成功時大致顯示：

~~~text
git version 2.x.x
~~~

你也可以使用 Windows 的套件管理器（已有 winget 時）：

~~~powershell
winget install --id Git.Git -e --source winget
~~~

Git Bash 是可以操作 Git 的終端機；VS Code 是程式碼編輯器。安裝 Git 不等於安裝 VS Code，安裝 VS Code 也不代表所有電腦都有 Git。

### 2-2 macOS

有 Homebrew 時可輸入：

~~~bash
brew install git
git --version
~~~

也可以使用 Xcode Command Line Tools：

~~~bash
xcode-select --install
git --version
~~~

macOS 可能原本就有 Git；版本不需要與 Windows 完全一樣，但要能正常執行。

### 2-3 Linux

Ubuntu／Debian：

~~~bash
sudo apt update
sudo apt install git
git --version
~~~

Fedora：

~~~bash
sudo dnf install git
git --version
~~~

### 2-4 終端機基本操作

Git 指令要在正確的資料夾執行；先熟悉這三個命令。

| 指令 | 用途 |
| --- | --- |
| <code>pwd</code> | 查看目前位置（Git Bash、macOS、Linux） |
| <code>ls</code> | 列出資料夾內容（Git Bash、macOS、Linux） |
| <code>cd 資料夾</code> | 進入指定資料夾 |

Windows PowerShell 可以用 <code>Get-Location</code> 看路徑、<code>Get-ChildItem</code> 看檔案，也能使用 <code>cd</code>。

### 練習與驗收

- 開啟 Git Bash 或終端機，執行 <code>git --version</code>。
- 說出自己使用哪個作業系統、哪個終端機。
- 若顯示「git 不是可辨識的命令」或「command not found」，先重新開啟終端機，確認 Git 安裝成功與 PATH 設定。

---

## 單元三｜GitHub 帳號與 Git 第一次設定

### 3-1 建立 GitHub 帳號

1. 前往 [GitHub](https://github.com/) 選擇 **Sign up**，依照畫面建立帳號；已經有帳號就選 **Sign in**。
2. 確認電子郵件並完成網站要求的驗證。
3. 建議開啟雙因素驗證（2FA），避免只有密碼保護帳號。
4. 登入後，在右上角的 **＋ → New repository**，可以建立 Repo。

建 Repo 時常用選項：

- **Repository name**：例如 <code>git-notes-practice</code>。
- **Public**：公開可被任何人看到；**Private**：限定授權成員。
- **Add a README file**：新增專案說明。如果準備從已有 Commit 的本機新專案第一次 Push，示範時先不要勾選，避免兩端有不同的初始歷史。
- **.gitignore／License**：稍後再學；不要在不了解前直接把含有私人資料的檔案公開。

### 3-2 設定 Git Commit 作者資訊

在終端機輸入（換成你自己的資料）：

~~~bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
~~~

- <code>--global</code>：設定目前使用者的 Git 預設值，而不是只有某個 Repo。
- <code>user.name</code>：Commit 顯示的作者名稱，不是 GitHub 登入驗證。
- <code>user.email</code>：Commit 作者 Email，若希望隱藏私人 Email，可改用 GitHub 提供的 noreply Email（在 GitHub Email 設定頁查看自己的實際地址）。
- <code>init.defaultBranch main</code>：新的 <code>git init</code> 預設分支叫 <code>main</code>。

查詢是否設定成功：

~~~bash
git config --global --get user.name
git config --global --get user.email
git config --global --get init.defaultBranch
~~~

:::warning
**設定 user.name 和 user.email 並不是登入 GitHub。** 它們只負責替 Commit 標示作者。真正連接遠端 Repo 時還需要 HTTPS 或 SSH 驗證，請看下一單元。
:::

### 練習與驗收

1. 能區分 GitHub 帳號、Git 作者名稱和 Git 連線驗證。
2. 用 <code>git config --global --get</code> 讀出自己剛設定的值。
3. 說出 Public 與 Private Repo 的差異。

---

## 單元四｜讓本機 Git 與 GitHub 連線（HTTPS 與 SSH）

### 4-1 先選適合自己的方式

| 方式 | 適合誰 | 特色 |
| --- | --- | --- |
| HTTPS + Git Credential Manager | 第一次學 Git 的學生，**建議先選** | 複製 HTTPS 網址；需要存取私有 Repo 或 Push 時通常透過瀏覽器授權 |
| SSH Key | 經常使用終端機開發的人 | 建立自己的金鑰組，在 GitHub 登記公鑰；之後使用 SSH URL |
| Personal access token（PAT） | 特定工具或沒有其他驗證方式時 | 是敏感憑證，要設最小權限，不能寫進程式碼或對話 |

**GitHub 不接受直接使用網站帳號密碼來進行一般的 Git HTTPS Push 驗證。** 初學者優先使用 Git for Windows 提供的 Git Credential Manager（GCM）與瀏覽器登入，不必自己產生 Token。

### 4-2 方法 A：使用 HTTPS（建議先學）

先登入 GitHub 並建立一個 **沒有 README 的空白練習 Repo**。按綠色 **Code**，選 **HTTPS**，複製網址，格式例如：

~~~text
https://github.com/your-username/git-notes-practice.git
~~~

以後在本機專案連接遠端時會輸入：

~~~bash
git remote add origin https://github.com/your-username/git-notes-practice.git
~~~

這一行只是登記遠端網址，**不會立即驗證帳號，也不會上傳檔案**。等執行 <code>git push</code> 等需要權限的操作時，Git Credential Manager 才可能顯示登入／授權畫面。確認帳號與要求的權限後，依畫面完成登入。

在 Windows 安裝 Git for Windows 時通常也會有 GCM。如果沒有跳出登入畫面，先確認使用的是 HTTPS URL、GCM 是否已安裝，以及終端機的錯誤訊息。

### 4-3 方法 B：使用 SSH 金鑰（延伸）

以 **Git Bash（Windows）或 macOS／Linux 終端機**示範，先檢查：

~~~bash
ls -al ~/.ssh
~~~

如果已經有 SSH 金鑰，先確認用途，**不要直接覆寫原有金鑰**。尚未建立可用金鑰時：

~~~bash
ssh-keygen -t ed25519 -C "you@example.com"
~~~

把 Email 換成自己的 GitHub Email。依提示選擇存放路徑並設定安全的 passphrase（私鑰密碼）。預設可能會得到：

~~~text
~/.ssh/id_ed25519       ← 私鑰：永遠不要公開
~/.ssh/id_ed25519.pub   ← 公鑰：可以貼到 GitHub
~~~

在終端機顯示**公鑰**內容：

~~~bash
cat ~/.ssh/id_ed25519.pub
~~~

進入 GitHub：**Settings → SSH and GPG keys → New SSH key**，選擇驗證用金鑰（Authentication key），將剛才的完整公鑰貼入並儲存。

確認 SSH 連線：

~~~bash
ssh -T git@github.com
~~~

第一次連線可能詢問伺服器指紋，**應先與 GitHub 官方公布的指紋核對**，不要不看內容就輸入 yes。成功大致顯示：

~~~text
Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
~~~

這是正常成功訊息；GitHub 不提供互動 Shell。此測試指令成功時也可能回傳結束碼 1，不要單看結束碼判定失敗。

建立遠端連線時，把 HTTPS URL 換成 SSH 格式：

~~~bash
git remote add origin git@github.com:your-username/git-notes-practice.git
~~~

:::warning
**切勿上傳或分享 <code>id_ed25519</code> 私鑰、PAT、密碼或登入 Cookie。** 只把 <code>.pub</code> 公鑰加入 GitHub。使用學校或公用電腦時，應確認帳號與登入權限，離開前安全登出。
:::

### 練習與驗收

1. 在 GitHub 的 Code 按鈕找出 HTTPS 與 SSH 兩種網址。
2. 說出 <code>git remote add origin</code> 和 <code>git push</code> 的差別。
3. SSH 使用者能指出哪份是私鑰、哪份是公鑰；HTTPS 使用者能解釋為什麼不該輸入 GitHub 網站密碼當成 Git 密碼。

官方參考：[GitHub HTTPS 憑證管理](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git)、[GitHub SSH 設定](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)、[SSH 測試](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)。

---

## 單元五｜建立第一個 Git 專案：init、add、commit

接下來終於實際操作 Git！**使用新的練習資料夾，不要在已存在的 ScoreSense Repo 裡再次執行 git init。** 以下指令使用 Git Bash、macOS 或 Linux 終端機；Windows PowerShell 也能執行相同的 Git 指令。

### 5-1 建立練習資料夾

~~~bash
mkdir git-practice
cd git-practice
git init
~~~

逐行解釋：

- <code>mkdir git-practice</code>：建立資料夾。若已存在，請換一個新名稱。
- <code>cd git-practice</code>：進入練習資料夾。
- <code>git init</code>：在這個資料夾建立 Git 版本庫。Git 會建立隱藏的 <code>.git</code> 目錄，保存歷史與設定。

確認狀態：

~~~bash
git status
~~~

初次初始化、還沒 Commit 時，通常會看到：

~~~text
On branch main
No commits yet
nothing to commit
~~~

如果尚未完成單元三的 <code>init.defaultBranch</code> 設定，預設分支名稱可能不同。請以終端機實際輸出為準。

### 5-2 新增一個 Python 檔案

用 VS Code 開啟這個資料夾，建立 <code>hello.py</code>：

~~~python
print("Hello, Git!")
~~~

再執行：

~~~bash
git status
~~~

你應該會在 **Untracked files（尚未追蹤）** 找到 <code>hello.py</code>。這代表 Git 看見新檔，但還沒有準備提交。

### 5-3 暫存修改：git add

~~~bash
git add hello.py
git status
~~~

這次 <code>hello.py</code> 應出現在 **Changes to be committed（準備提交）** 下。

~~~text
工作目錄：hello.py 新檔
        │
        └── git add hello.py ──→ 暫存區
~~~

使用 <code>git add hello.py</code> 明確指定檔案，適合初學者。<code>git add .</code> 會一次加入目前目錄下的多個變更，專案有密碼、產生檔或私人資料時可能不小心一起加入；應先檢查 <code>git status</code> 再決定。

### 5-4 建立第一次 Commit

~~~bash
git commit -m "feat: 新增第一支 Python 練習程式"
~~~

- <code>commit</code>：把暫存區的內容存成新的本機版本紀錄。
- <code>-m</code>：直接在指令後附上這筆 Commit 的說明。
- <code>feat:</code>：常見的 Commit 命名方式，表示新增功能；也可使用 <code>fix:</code>（修正）或 <code>docs:</code>（文件）。

成功輸出通常包含短 SHA、檔案變更數等，例如：

~~~text
[main (root-commit) abc1234] feat: 新增第一支 Python 練習程式
 1 file changed, 1 insertion(+)
 create mode 100644 hello.py
~~~

<code>abc1234</code> 是示意值，每個人的 Commit ID 都不同。

再執行：

~~~bash
git status
git log --oneline
~~~

若沒有新修改，狀態應顯示類似 <code>nothing to commit, working tree clean</code>；Log 會列出剛剛的紀錄。

### 5-5 再改一次，觀察差別

把 <code>hello.py</code> 修改成：

~~~python
print("Hello, Git!")
print("This is version 2.")
~~~

依序執行：

~~~bash
git status
git diff
git add hello.py
git diff --staged
git commit -m "feat: 加入第二行輸出"
~~~

這裡有兩個不同的比較：

- <code>git diff</code>：檢視**尚未暫存**的檔案變更。
- <code>git diff --staged</code>：檢視**已加入暫存區、下一次 Commit 將包含**的變更。

### 小練習與驗收

1. 用自己的話解釋 <code>git add</code> 和 <code>git commit</code> 的不同。
2. 建立 <code>notes.txt</code>，先不要 add，預測 <code>git status</code> 會看到什麼。
3. 為 <code>notes.txt</code> 建立 Commit，再查詢 Log。
4. 說明「Commit 是本機紀錄」和「GitHub 上傳」為什麼是兩件事。

---

## 單元六｜將本機專案上傳 GitHub：remote 與 push

前一單元的兩個 Commit **目前只在自己的電腦**。這一單元把它們傳到 GitHub。

### 6-1 準備一個空的 GitHub Repository

在 GitHub 右上角 **＋ → New repository**：

1. Repository name 輸入 <code>git-notes-practice</code>。
2. 選 Public 或 Private（練習時建議先選 Private）。
3. **不要先新增 README、.gitignore、License**，保持空白。
4. 點選 **Create repository**，複製 HTTPS URL。

假設你的 GitHub 帳號叫 <code>your-username</code>，網址會像：

~~~text
https://github.com/your-username/git-notes-practice.git
~~~

### 6-2 連接 origin

回到前一單元的 <code>git-practice</code> 資料夾：

~~~bash
git remote add origin https://github.com/your-username/git-notes-practice.git
git remote -v
~~~

**一定要把 your-username 換成自己的帳號！**

- <code>remote</code>：管理與其他版本庫的連線紀錄。
- <code>add</code>：新增一個遠端位置。
- <code>origin</code>：自行取的遠端名稱；Git 慣例使用它代表主要遠端。
- <code>remote -v</code>：查看 Fetch 與 Push 使用的遠端 URL。

如果出現 <code>remote origin already exists</code>，代表已有同名遠端。先執行 <code>git remote -v</code> 看清楚位置；確認真的填錯後，才用以下指令修改：

~~~bash
git remote set-url origin https://github.com/your-username/git-notes-practice.git
~~~

### 6-3 第一次 Push

我們要把本機分支統一叫作 <code>main</code>：

~~~bash
git branch -M main
git push -u origin main
~~~

說明：

- <code>git branch -M main</code>：將**目前分支**重新命名為 main，必要時強制取代同名本機分支。這裡只適用於全新練習 Repo，已存在的正式專案不要照抄。
- <code>git push</code>：將本機 Commit 發送到遠端。
- <code>-u</code>：設定追蹤關係（upstream），之後在同一分支通常可直接執行 <code>git push</code>。
- <code>origin main</code>：指定遠端名稱與要推送的分支。

首次 HTTPS Push 時，可能開啟 Git Credential Manager 的瀏覽器登入流程。登入後 GitHub Repo 應能看見 <code>hello.py</code>、<code>notes.txt</code>（若已 Commit）以及 Commit 紀錄。

### 6-4 日常更新的最小流程

之後每次改完一個小功能：

~~~bash
git status
git add hello.py
git commit -m "fix: 修正顯示文字"
git push
~~~

若和其他人協作，在開始修改前應先確認遠端更新，通常會先用 <code>git pull</code> 同步；下一單元會學。

:::warning
**上傳前先確認公開範圍。** 即使之後刪除檔案，敏感內容仍可能存在 Git 歷史裡。包含密碼、Token、學生成績或私人資料的檔案不應提交。不要使用 <code>git push --force</code> 來處理一般 Push 問題。
:::

### 小練習與驗收

1. 使用 <code>git remote -v</code> 確認遠端 URL 是自己的 Repo。
2. 找出 GitHub 網站上的第一筆 Commit。
3. 再修改一行 <code>hello.py</code>，Commit 並 Push，確認網站已更新。
4. 回答：只有 <code>git add</code>，但沒有 Commit，<code>git push</code> 能上傳新修改嗎？（不能。）

---

## 單元七｜下載與同步專案：clone、pull、fetch

### 7-1 clone：第一次取得遠端專案

如果要在另一台電腦使用 GitHub 的專案，通常從 <code>git clone</code> 開始。

先切換到**你想放置專案的上層資料夾**（不可直接克隆到已經裝有其他專案的非空資料夾），輸入：

~~~bash
git clone https://github.com/your-username/git-notes-practice.git
~~~

Git 會建立同名資料夾，包含程式碼與版本歷史。進入：

~~~bash
cd git-notes-practice
git status
git remote -v
~~~

<code>clone</code> 後不必再執行 <code>git init</code> 或 <code>git remote add origin</code>，因為 Git 已經設定好這個版本庫的歷史與遠端資訊。

### 7-2 pull：下載並整合遠端更新

例如同學在 GitHub 上更新 <code>README.md</code>，你要把修改帶回本機：

~~~bash
git status
git pull --ff-only
~~~

- <code>git pull</code>：先從遠端 Fetch，再整合到目前分支。
- <code>--ff-only</code>：只在能快轉（fast-forward）時整合；若本機與遠端歷史已分岔，會停止而不是自動產生合併 Commit。

初學者使用 <code>--ff-only</code> 可避免不明白狀況就自動合併。這要先有上游追蹤分支（例如前一單元的 <code>push -u</code> 或 <code>clone</code>）。

若本機有未提交的修改，Pull 可能被 Git 阻止，或造成後續衝突；**先檢查 status 並妥善 Commit 或保存修改**，不要為了讓指令成功就直接刪除檔案。

### 7-3 fetch：只取得資料，先不動你的程式

~~~bash
git fetch origin
git log --oneline --decorate --all -n 8
~~~

<code>fetch</code> 會更新本機對遠端分支的參考，例如 <code>origin/main</code>，**不會直接改寫你目前的工作目錄**。

比較本機 main 與遠端的變更：

~~~bash
git log --oneline main..origin/main
git diff main..origin/main
~~~

第一個指令列出遠端有、目前本機 main 尚未有的 Commit；第二個顯示兩者檔案內容差異。若目前不在 main，應依實際分支調整指令。

### 7-4 三個指令不要搞混

| 指令 | 本機檔案會改變嗎？ | 什麼時候用 |
| --- | --- | --- |
| <code>git clone</code> | 會建立一份新專案 | 第一次下載 Repo |
| <code>git fetch</code> | 不直接改目前工作檔 | 先查詢遠端新紀錄 |
| <code>git pull</code> | 成功整合後可能改變 | 同步目前分支到遠端最新版本 |

### 小練習與驗收

1. 將自己 GitHub 的練習 Repo clone 到另一個**全新**資料夾。
2. 在 GitHub 網站編輯練習 Repo 的檔案並提交；回到 clone 出來的資料夾，先 <code>git fetch</code>、檢查差異，再 <code>git pull --ff-only</code>。
3. 分辨 clone、fetch、pull 各自的用途。

---

## 單元八｜Git 常用指令與版本紀錄：status、diff、log、show

### 8-1 經常使用的四個檢查指令

~~~bash
git status
git diff
git log --oneline -n 5
git show HEAD
~~~

| 指令 | 會看到什麼 |
| --- | --- |
| <code>git status</code> | 目前所在分支、未追蹤、未暫存、已暫存的檔案 |
| <code>git diff</code> | 工作目錄中尚未暫存的內容變化 |
| <code>git log --oneline -n 5</code> | 最近五筆 Commit 的簡短紀錄 |
| <code>git show HEAD</code> | 目前最新 Commit 的資訊與變更內容 |

<code>HEAD</code> 通常代表目前 checkout 的 Commit；不是一個固定不變的 Commit ID。

### 8-2 認識差異輸出

~~~diff
-print("Hello")
+print("Hello, Git")
~~~

- 開頭 <code>-</code>：相較於比較基準，被移除的那一行。
- 開頭 <code>+</code>：相較於比較基準，被新增的那一行。
- 這裡不代表一定刪掉整個檔案，而是在比較檔案的文字內容。

再試：

~~~bash
git diff --staged
git show --stat HEAD
git log --oneline --graph --all
~~~

- <code>--staged</code>：比較暫存區與最新 Commit。
- <code>--stat</code>：顯示變更檔案與增減行數摘要。
- <code>--graph --all</code>：用文字圖顯示多個分支的 Commit 歷史。

### 8-3 如何寫讓人看得懂的 Commit Message？

不好：

~~~text
更新
123
修改
final final
~~~

較好：

~~~text
feat: 新增圖片檔案大小檢查
fix: 修正空檔案造成的例外
docs: 補充本機執行說明
~~~

常見的前綴：

- <code>feat</code>：新增功能。
- <code>fix</code>：修正問題。
- <code>docs</code>：只改文件。
- <code>test</code>：新增或修改測試。
- <code>refactor</code>：重整程式結構，目的不在改變功能。

### 8-4 指令速查表（建議當作日常書籤）

| 指令 | 主要用途 | 初學者提醒 |
| --- | --- | --- |
| <code>git init</code> | 建立本機 Repo | 已 clone 的專案不需再 init |
| <code>git clone URL</code> | 下載 Repo | URL 要確認來源 |
| <code>git status</code> | 查詢變更狀態 | **每次操作前先看** |
| <code>git add 檔名</code> | 選取要提交的修改 | 避免加入私密檔 |
| <code>git commit -m "訊息"</code> | 建立版本紀錄 | 不會自動上傳 |
| <code>git log --oneline</code> | 查看歷史 | 查看短 SHA |
| <code>git diff</code> | 查看未暫存差異 | 可先確認程式變了什麼 |
| <code>git diff --staged</code> | 查看已暫存差異 | Commit 前再檢查 |
| <code>git remote -v</code> | 查看遠端 | 檢查有沒有連錯 Repo |
| <code>git push</code> | 上傳 Commit | 先確認遠端和分支 |
| <code>git pull --ff-only</code> | 安全快轉同步 | 分岔時需先處理 |
| <code>git fetch</code> | 只取得遠端資料 | 不直接更動工作檔 |
| <code>git branch</code> | 列出本機分支 | 星號是目前所在分支 |
| <code>git switch 分支名</code> | 切換分支 | 先確認未提交修改 |
| <code>git merge 分支名</code> | 合併分支 | 先確認合併目標 |
| <code>git restore 檔名</code> | 還原未暫存修改 | **可能遺失修改** |
| <code>git revert SHA</code> | 用新 Commit 反向撤銷變更 | 較適合已分享的歷史 |

### 小練習與驗收

1. 看 Log 找到最新一筆 Commit 的訊息與短 SHA。
2. 修改一行檔案，用 <code>git diff</code> 看出差別，但先不要 Commit。
3. 將修改加到暫存區後，再比較 <code>git diff</code> 與 <code>git diff --staged</code> 的輸出。

---

## 單元九｜Branch 分支與 Pull Request：多人協作的核心

### 9-1 為什麼需要分支？

如果你正在修正 ScoreSense 的一個 Bug，但朋友同時在寫新功能，兩個人一直修改 main 就可能互相干擾。

~~~text
main:     A ── B ───────────── E
               \              /
feature:        C ── D ───────
~~~

- <code>main</code>：通常保存主要、可使用的版本。
- <code>feature/...</code>：新的工作分支，供開發者獨立修改。
- 完成後提出 **Pull Request（PR，合併請求）**，請他人檢查，再決定是否合併回 main。

Branch 是 Git 功能；GitHub 的 Pull Request 是建立在分支與版本比較之上的協作功能。

### 9-2 建立並切換到新分支

先確認目前狀態：

~~~bash
git status
git branch
~~~

假設目前在 main，且工作目錄沒有未提交修改：

~~~bash
git switch -c feature/add-note
git branch
~~~

- <code>switch</code>：切換到指定分支。
- <code>-c</code>：建立新分支並切換過去。
- <code>feature/add-note</code>：可自行取名；建議用簡短、可讀的英文名稱。

再新增 <code>feature_note.txt</code>，內容輸入一行文字。接著：

~~~bash
git add feature_note.txt
git commit -m "feat: 新增分支練習筆記"
git push -u origin feature/add-note
~~~

這次 Push 的是**新分支**，不是 main。

### 9-3 在 GitHub 建立 Pull Request

1. 前往自己剛剛的 GitHub Repo。
2. 找到分支更新提示並選擇 **Compare & pull request**；如果沒有提示，可以從 **Pull requests → New pull request** 開始。
3. **base** 選 <code>main</code>，**compare** 選 <code>feature/add-note</code>。
4. 填寫標題與描述，例如「新增筆記說明」，解釋變更內容與測試情況。
5. 點 **Create pull request**。
6. 查看 **Files changed**、留言與 GitHub Checks 的結果；確認後才使用 **Merge pull request**（前提是你有權限且符合專案規則）。

:::info
第一次學習時，請只在自己的練習 Repo 建 PR。正式團隊常要求同學審查、測試通過或主分支受保護，不能只因為出現 Merge 按鈕就按下去。
:::

### 9-4 合併完成後同步本機

如果 PR 已經在 GitHub 合併回 main：

~~~bash
git switch main
git pull --ff-only
~~~

本機 main 更新完成後，才可以評估是否刪除完成工作的本機分支：

~~~bash
git branch -d feature/add-note
~~~

<code>-d</code> 在 Git 判斷分支尚未安全合併時可能拒絕刪除；請先查明原因。**不要改用 <code>-D</code> 強行刪除仍有獨立成果的分支。**

### 9-5 簡單認識 git merge

假設你有兩個本機分支，正在 <code>main</code>，要把 <code>feature/add-note</code> 合併進來：

~~~bash
git switch main
git merge feature/add-note
~~~

注意：<code>git merge 後面的分支</code> 是**要合併進目前所在分支**的來源，而不是要切換過去的分支。在 GitHub 的 PR 協作流程中，通常由平台完成合併，不一定需要自行執行本機 merge。

### 小練習與驗收

1. 建立 <code>feature/readme</code> 分支，修改練習 Repo 裡的 README。
2. 用 <code>git branch</code> 確認現在在哪個分支。
3. 將該分支 Push 到遠端後，在 GitHub **比較差異**；不必一定進行合併。
4. 說出 PR 的 base 與 compare 分別代表什麼。

---

## 單元十｜版本還原、衝突與錯誤處理

這一單元最重要的是：**看到一個可以修復問題的指令，不代表可以毫無確認直接執行。** 在實際專案中，先找出修改是否已 Commit、是否 Push，以及是否有其他人的變更。

### 10-1 三種容易混淆的還原

| 指令 | 適用情況 | 對修改的影響 |
| --- | --- | --- |
| <code>git restore hello.py</code> | 捨棄尚未暫存的本機修改 | **會失去指定檔案的未暫存修改** |
| <code>git revert SHA</code> | 撤銷某個已提交的 Commit | 建立新的反向 Commit，保留原有歷史（可能產生衝突） |
| <code>git reset</code> | 移動分支／HEAD，通常用於整理尚未分享的本機歷史 | 行為依參數而不同；某些模式會丟失資料 |

**初學者不要把 <code>git reset --hard</code> 當成萬用修復指令。** 它會重置追蹤檔案的工作區與暫存區，可能刪掉尚未 Commit 的成果。

### 10-2 情境 A：只改錯了一行，還沒 git add

先看差異：

~~~bash
git status
git diff -- hello.py
~~~

確定這些修改真的全部不要時，才執行：

~~~bash
git restore -- hello.py
~~~

<code>--</code> 用來區分參數與檔案路徑。還原後再查 <code>git status</code>。**如果你其實想保留另一半修改，不要直接 restore 整份檔案。**

### 10-3 情境 B：不小心 git add，但還沒有 Commit

若只是想把檔案從暫存區移除，保留工作目錄裡的修改：

~~~bash
git restore --staged -- hello.py
git status
~~~

<code>--staged</code> 指定操作暫存區，不是讓工作檔案消失；仍應檢查目前狀態。

### 10-4 情境 C：已經 Commit（甚至已 Push）

先查 Log：

~~~bash
git log --oneline -n 5
~~~

假設想撤銷的 Commit 是 <code>abc1234</code>（只是範例，請用自己的真實 SHA）：

~~~bash
git revert abc1234
~~~

Git 會建立一筆新的反向紀錄；如果遇到衝突，要先處理衝突才能完成。**不要在不了解影響時直接對正式 main 執行。**

### 10-5 git reset 要懂，但先不要在正式專案亂用

~~~bash
git reset --soft HEAD~1
~~~

這個範例會將目前分支指標移回上一個 Commit，同時保留原先的修改在暫存區。它會改寫**本機分支歷史**；適合尚未 Push 且完全理解狀態的情況。若已經把 Commit 分享給別人，應優先考慮 <code>revert</code>，避免重寫公共歷史。

### 10-6 合併衝突是什麼？

兩個人同時修改了同一個檔案的相近內容，Git 可能無法自動決定誰的版本應該保留。下面左側的 1～5 是教學用行號，實際衝突檔案**不會有這些行號**。

~~~text
1  <<<<<<< HEAD
2  print("Hello from main")
3  =======
4  print("Hello from feature")
5  >>>>>>> feature/add-note
~~~

這些標記代表：

- <code><<<<<<< HEAD</code> 到分隔線：目前版本的片段。
- <code>=======</code>：兩種內容的分界。
- <code>>>>>>> feature/add-note</code>：另一個分支的片段。

實際操作：

1. 執行 <code>git status</code>，找出衝突檔案。
2. 用 VS Code 開啟衝突檔，決定保留哪一邊或重新整理兩邊內容。
3. 移除所有衝突標記，保存檔案並確認程式仍然可執行。
4. 執行 <code>git add 衝突檔名</code>。
5. 如果是一般 merge，執行 <code>git merge --continue</code>；若是 rebase 或 revert，依 Git 顯示的提示執行對應的 <code>--continue</code>。不同操作不要混用。
6. 不確定怎麼解時，可先查看狀態並請教同學；某些操作可用 <code>git merge --abort</code> 取消進行中的合併。

### 10-7 常見錯誤對照表

| 訊息／問題 | 常見原因 | 優先處理 |
| --- | --- | --- |
| <code>fatal: not a git repository</code> | 在錯的資料夾下指令 | 用 <code>pwd</code> 或 <code>Get-Location</code> 確認位置 |
| <code>nothing to commit</code> | 沒有新修改或修改尚未被追蹤 | 用 <code>git status</code> 確認 |
| <code>Author identity unknown</code> | Git 作者未設定 | 設定 <code>user.name</code>、<code>user.email</code> |
| <code>remote origin already exists</code> | 已有 origin 設定 | 先 <code>git remote -v</code>，確認後再調整 |
| <code>Permission denied (publickey)</code> | SSH Key 未登記／未載入，或存取權不足 | 檢查公鑰與登入帳號、<code>ssh -T</code> |
| <code>Authentication failed</code> | HTTPS 授權或憑證問題 | 用 GCM 重新授權，確認帳號與 Repo 權限 |
| <code>non-fast-forward</code> / <code>rejected</code> | 遠端已有本機沒有的 Commit | Fetch、檢查差異，安全整合後再 Push |
| <code>CONFLICT</code> | 修改互相衝突 | 按上面步驟人工確認，不要強制覆蓋 |
| 檔案在 GitHub 沒更新 | 只 Add/Commit、Push 錯分支或 Push 失敗 | <code>git status</code>、<code>git branch</code>、<code>git remote -v</code> |
| GitHub Pages 沒立即更新 | 建置或部署仍在進行／失敗 | 到 GitHub **Actions** 查看對應 workflow 與日誌 |

### 小練習與驗收

1. **只在練習 Repo 中**修改一行尚未 Commit 的文字，先看 Diff，再用 <code>git restore</code> 還原。
2. 另一次修改後，執行 <code>git add</code>，再用 <code>git restore --staged</code> 取消暫存，確認檔案修改仍在。
3. 能說出「restore、revert、reset」三者的差別，以及為什麼不應隨意 <code>reset --hard</code>。

---

## 單元十一｜.gitignore、敏感資訊與專案整潔

### 11-1 哪些檔案適合 Commit？

一般應提交：

- 自己寫的 <code>.py</code> 程式與經允許分享的設定範例。
- 可公開的 <code>README.md</code>、測試程式與必要的小型測試素材。
- 讓別人能重建環境的 <code>requirements.txt</code>（但不是整個虛擬環境）。

一般不應提交：

- 真實密碼、API Key、存取 Token、Cookie、SSH 私鑰。
- <code>.venv/</code>、Python <code>__pycache__/</code>、<code>*.pyc</code>。
- 個人機密檔、使用者上傳的檔案、非必要的大型輸出或模型快取。
- 含私人資訊的日誌、帳號設定與資料庫。

### 11-2 建立 .gitignore

在專案根目錄新增 <code>.gitignore</code>：

~~~gitignore
# Python 產生檔與虛擬環境
.venv/
venv/
__pycache__/
*.pyc

# 本機秘密與環境設定
.env
.env.*
!.env.example

# 本機產物
outputs/
*.log

# 編輯器個人設定（是否忽略可依團隊決定）
.vscode/
~~~

解釋：

- <code>#</code>：註解。
- <code>.venv/</code>：忽略這個名稱的虛擬環境資料夾。
- <code>*.pyc</code>：忽略符合副檔名的檔案。
- <code>!.env.example</code>：允許追蹤**不含秘密**的範例設定檔。

檢查：

~~~bash
git status
git check-ignore -v .venv/example.txt
~~~

後者顯示 Git 是依哪條忽略規則跳過該路徑；檔案不存在時的顯示情況可能因路徑與設定不同。

### 11-3 已經被追蹤的檔案，加 .gitignore 就夠了嗎？

**不夠。** <code>.gitignore</code> 主要影響未追蹤的檔案，已經 Commit 過的檔案不會自動從 Git 歷史消失。

若某個一般設定檔原本已被追蹤，但現在只想保留在本機：

~~~bash
git rm --cached path/to/local-settings.json
~~~

它會從索引中移除這個檔案，但不會直接刪掉目前工作目錄內的檔案。接著調整 <code>.gitignore</code>、檢查 Diff，再 Commit。**這仍不能消除早期 Commit 中已經公開的內容。**

如果密碼或 Token 曾被 Push 到 GitHub：

1. **立即撤銷／輪替該憑證**，不要只刪檔就以為安全。
2. 判斷是否需要依官方程序移除 Git 歷史中的敏感資料。
3. 通知相關負責人，評估是否有其他地方複製了憑證。
4. 在沒有確認影響前，不要自行改寫共同分支的公開歷史。

### 11-4 為什麼 README 很重要？

README 是打開 GitHub Repo 時最容易看到的專案說明。至少可以寫：

~~~markdown
# 我的 Python 練習

這是一個用來練習 Git 與 Python 的小型專案。

## 執行方式

1. 安裝 Python。
2. 在專案資料夾執行 `python hello.py`。

## 注意事項

不需要上傳 .venv，其他人可以建立自己的環境。
~~~

### 小練習與驗收

1. 建立一個 <code>.gitignore</code> 並輸入上述規則。
2. 在練習資料夾建立 <code>.env</code>（**只填入假資料**），確認 <code>git status</code> 不會顯示它作為可新增的檔案。
3. 說明為什麼 <code>.gitignore</code> 不能取代對真正洩漏憑證的輪替。

---

## 單元十二｜VS Code 圖形化 Git 與 GitHub 常用功能

前面使用終端機是為了看懂 Git 究竟做了什麼。日常寫程式也可以用 **VS Code Source Control（原始檔控制）** 介面完成多數操作。

### 12-1 在 VS Code 開啟 Git 專案

1. 用 VS Code 的 **File → Open Folder** 開啟包含 <code>.git</code> 的資料夾。
2. 左側點選 **Source Control** 圖示（分支狀的圖案）；Windows 常用快捷鍵 <code>Ctrl+Shift+G</code>。
3. 如果 VS Code 提示找不到 Git，先用單元二確認安裝並重新啟動 VS Code。

### 12-2 從修改到 Commit

1. 開啟 <code>hello.py</code>，改動一行，並**儲存檔案**。
2. 在 **Changes** 清單找到檔案，點選檔名查看差異。
3. 按檔案旁的 **＋（Stage Changes）** 把修改加入暫存區。
4. 在上方輸入 Commit Message，例如 <code>docs: 更新練習說明</code>。
5. 按 **Commit** 建立本機版本紀錄。
6. 用 **Sync Changes** 或 **Push** 上傳；注意 VS Code 的 **Sync Changes** 可能同時執行 Pull 與 Push，不能把它當成只上傳的按鈕。

| 終端機指令 | VS Code 大致相對應操作 |
| --- | --- |
| <code>git status</code> | Source Control 變更清單 |
| <code>git diff</code> | 點選檔案的 Diff 檢視 |
| <code>git add hello.py</code> | Stage Changes（＋） |
| <code>git commit</code> | 輸入訊息 → Commit |
| <code>git push</code> | Push 選單項目 |
| <code>git pull</code> | Pull 選單項目 |
| <code>git switch</code> | 左下角分支名稱／分支選單 |

VS Code 版本與安裝的擴充套件會影響介面名稱；若找不到按鈕，先確認開啟的是正確 Repo，再查看 Source Control 的 **…** 選單。

### 12-3 GitHub 常用頁面

| 頁面／功能 | 用途 |
| --- | --- |
| **Code** | 看原始碼、分支、下載／複製 Repo URL |
| **Commits** | 追蹤誰改了哪些內容 |
| **Pull requests** | 提出、審查與合併變更 |
| **Issues** | 記錄 Bug、工作項目、待辦與討論 |
| **Actions** | 查看自動測試、建置、部署的結果 |
| **README** | 說明專案目的、安裝與使用方式 |
| **Settings** | 權限、Repo 設定與 Pages 設定（需有對應權限） |
| **GitHub Pages** | 將靜態網站透過 GitHub 發布 |

### 12-4 GitHub Actions 與 Pages：連回 ScoreSense

ScoreSense 的教學網站正是以 GitHub Pages 發布的。它使用 GitHub Actions 在 main 收到 Push 後建立靜態教材並部署。

~~~text
修改教學 Markdown
        ↓
Commit + Push 至 main
        ↓
GitHub Actions 建置教材
        ↓
部署 GitHub Pages
        ↓
學生重新整理教學網站
~~~

因此即使 Git Push 成功，**也不等於網站已部署完成**。如果網站沒有更新，應到 Repo 的 **Actions** 查看對應 Workflow 的狀態與錯誤日誌。這是一個認識「版本控制」與「網站部署」差異的實際例子。

### 小練習與驗收

1. 用 VS Code 的 Source Control 介面查看一次修改差異。
2. 說出 Stage、Commit、Push 在圖形介面中的位置；不必真的修改正式 ScoreSense Repo。
3. 打開任一個有權查看的 Repo，找出 **Commits、Pull requests、Issues、Actions**。
4. 回答：「GitHub Pages 沒更新時，為什麼不能只一直按重新整理？」（因為部署可能還沒有成功。）

---

## 附錄 A｜Git 指令該在什麼狀況使用？

| 我現在想做什麼？ | 可以先使用 |
| --- | --- |
| 確認現在改了哪些檔案 | <code>git status</code> |
| 檢視尚未暫存的差異 | <code>git diff</code> |
| 準備好某個檔案要加入下一次 Commit | <code>git add 檔名</code> |
| 保存目前階段的本機版本 | <code>git commit -m "說明"</code> |
| 將已提交的版本送到 GitHub | <code>git push</code> |
| 第一次在新電腦取得 Repo | <code>git clone URL</code> |
| 知道 GitHub 有沒有新版本 | <code>git fetch</code> |
| 讓本機同步遠端、只允許快轉 | <code>git pull --ff-only</code> |
| 查詢歷史 | <code>git log --oneline</code> |
| 進行新功能但不想直接碰 main | <code>git switch -c feature/名稱</code> |
| 在 GitHub 請同學審查修改 | 提出 Pull Request |
| 還原單一檔案未暫存的改動 | **先確認不需要保留後** <code>git restore -- 檔名</code> |
| 安全撤銷已分享的特定 Commit | 評估使用 <code>git revert SHA</code> |
| 檢查 Repo 有沒有設錯遠端 | <code>git remote -v</code> |

## 附錄 B｜中英文關鍵名詞

| 英文 | 中文 | 快速記憶 |
| --- | --- | --- |
| Version control | 版本控制 | 追蹤版本如何變化 |
| Distributed | 分散式 | 本機就有可操作的版本歷史 |
| Working tree | 工作樹 | 目前實際看到的專案檔案 |
| Index / Staging area | 索引／暫存區 | 下一次 Commit 的候選內容 |
| Untracked | 未追蹤 | Git 看到但尚未納入追蹤的新檔 |
| Commit | 提交 | 記錄一個版本狀態 |
| SHA / Commit ID | 提交識別碼 | 對應特定 Commit |
| HEAD | 目前檢出位置 | 通常指向目前 Commit |
| Branch | 分支 | 同一 Repo 的不同開發路線 |
| main | 主分支名稱 | 常用慣例，不是所有 Repo 都叫 main |
| origin | 遠端別名 | 預設習慣名稱，可以更換 |
| upstream | 上游追蹤分支 | 本機分支平時同步的對象 |
| Push / Pull | 推送／拉取 | 向遠端送出／取得並整合變更 |
| Fetch | 擷取 | 只先取得遠端物件與參考 |
| Merge | 合併 | 整合不同分支歷史 |
| Conflict | 衝突 | Git 無法自動判斷如何合併 |
| Pull Request (PR) | 合併請求 | 請其他人討論與審查修改 |
| Authentication | 身分驗證 | 證明你是誰 |
| Authorization | 授權 | 決定你可以做哪些動作 |
| CI / CD | 持續整合／持續交付部署 | 自動測試、建置及發布流程 |

## 本章檢核｜不用背誦，但要會判斷

請試著回答：

1. Git 與 GitHub 差在哪裡？如果網路中斷，哪些工作仍可進行？
2. 為什麼設定 <code>user.name</code> 不代表登入 GitHub？
3. <code>git add</code>、<code>git commit</code>、<code>git push</code> 分別負責哪一段？
4. <code>git clone</code>、<code>git fetch</code>、<code>git pull</code> 用在什麼不同情況？
5. 兩個人修改同一份檔案時，為什麼要用分支與 Pull Request？
6. 已 Push 的錯誤 Commit，為什麼不應直接強制改寫共同分支？
7. 為什麼 <code>.gitignore</code> 不能讓已經外洩的密碼變安全？
8. Push 成功但 Pages 尚未更新，你會去哪個頁面查原因？

### 完成本章後，你應該能做到

**自己安裝 Git、完成 GitHub 驗證、建立本機 Commit、更新 GitHub、查看歷史、使用分支和 PR，並知道遇到錯誤時先查什麼、哪些指令具有風險。**

這章沒有要求另外完成一個大型實戰專案；每個單元內的小練習就足以讓你逐步熟悉工具。

## 官方延伸閱讀

- [Git 官方下載與安裝](https://git-scm.com/downloads)
- [Pro Git 免費電子書](https://git-scm.com/book/en/v2)
- [Git 指令參考](https://git-scm.com/docs)
- [GitHub 入門教學](https://docs.github.com/en/get-started)
- [GitHub 設定 SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub Pull Request 教學](https://docs.github.com/en/pull-requests)
- [VS Code 版本控制說明](https://code.visualstudio.com/docs/sourcecontrol/overview)
