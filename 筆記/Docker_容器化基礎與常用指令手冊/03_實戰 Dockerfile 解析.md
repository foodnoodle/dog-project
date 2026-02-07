## 第三章：實戰 Dockerfile 解析

### 3.1 Dockerfile 的作用

Dockerfile 是一個純文字檔案，其中包含了一系列指令，告訴 Docker 如何自動化構建 (Build) 一個映像檔。Docker Daemon 會依照檔案中的指令，由上而下逐行執行，每一行指令都會產生一個新的 Layer（層）。

### 3.2 常用指令詳解

在 `dog-project` 中，主要使用了以下關鍵指令：

| 指令 | 說明 | 範例 |
| --- | --- | --- |
| **FROM** | 指定基礎映像檔 (Base Image)，決定作業系統與語言環境。 | `FROM python:3.9` |
| **WORKDIR** | 設定容器內的工作目錄 (類似 Linux 的 `cd` 指令)。 | `WORKDIR /app` |
| **COPY** | 將宿主機 (Host) 的檔案複製到容器內。 | `COPY requirements.txt .` |
| **RUN** | 在**建置階段 (Build Time)** 執行的指令，通常用於安裝套件。 | `RUN pip install django` |
| **CMD** | 指定容器**啟動階段 (Runtime)** 預設執行的指令。 | `CMD ["python", "manage.py", "runserver"]` |
| **EXPOSE** | 宣告容器預計監聽的連接埠 (僅作為文件說明，不具強制力)。 | `EXPOSE 8000` |

### 3.3 後端 Dockerfile 解析 (`backend/Dockerfile`)

以下是 `dog-project` 後端環境的標準建置邏輯分析：

```dockerfile
# 1. 基礎環境
# 使用 Python 3.9 的 slim 版本 (精簡版 Linux)，以減少映像檔體積
FROM python:3.9-slim

# 2. 設定工作目錄
# 之後所有的指令 (COPY, RUN, CMD) 都會在這個目錄下執行
WORKDIR /app

# 3. 安裝依賴 (利用 Layer 快取機制)
# 先只複製 requirements.txt，而不是複製所有程式碼
# 目的：只要 requirements.txt 沒變，Docker 就會使用快取，跳過 pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製程式碼
# 將本機 backend 資料夾的所有內容，複製到容器的 /app
COPY . .

# 5. 宣告端口
# 告訴開發者這個容器會使用 8000 port
EXPOSE 8000

# 6. 啟動指令
# 0.0.0.0 代表綁定所有網卡，這在 Container 中是必要的，否則外部無法連線
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 3.4 前端 Dockerfile 解析 (`frontend/Dockerfile`)

以下是 `dog-project` 前端環境 (Vue + Vite) 的標準建置邏輯分析：

```dockerfile
# 1. 基礎環境
# 使用 Node.js 18 的 alpine 版本 (極輕量 Linux)
FROM node:18-alpine

# 2. 設定工作目錄
WORKDIR /app

# 3. 安裝依賴
# 複製 package.json 與 package-lock.json
COPY package*.json ./
RUN npm install

# 4. 複製程式碼
COPY . .

# 5. 宣告端口
# Vite 預設開發端口為 5173
EXPOSE 5173

# 6. 啟動指令
# --host 0.0.0.0 是關鍵參數，允許容器被外部 (宿主機) 訪問
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### 3.5 構建映像檔 (Build Image)

撰寫完 Dockerfile 後，可透過以下指令將其轉換為映像檔：

```bash
# 語法：docker build -t <映像檔名稱> <Dockerfile所在路徑>

# 建置後端
docker build -t dog-backend ./backend

# 建置前端
docker build -t dog-frontend ./frontend
```