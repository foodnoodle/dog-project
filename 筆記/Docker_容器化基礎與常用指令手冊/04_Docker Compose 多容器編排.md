## 第四章：Docker Compose 多容器編排

### 4.1 什麼是 Docker Compose？

在真實的專案開發中，應用程式往往不是單一孤立的容器，而是由多個服務（如：後端 API、前端介面、資料庫、快取）共同組成的微服務架構。

Docker Compose 是一個用於定義和運行多容器 Docker 應用程式的工具。它使用 YAML 檔案 (`docker-compose.yaml`) 來配置應用程式的服務，並透過單一指令 (`docker-compose up`) 即可建立並啟動所有服務。

### 4.2 `docker-compose.yaml` 結構解析

以下針對 `dog-project` 專案中的 `docker-compose.yaml` 進行逐行解析，理解前後端如何被定義與連結。

```yaml
version: '3.8'  # Docker Compose 檔案格式版本

services:
  # --- 後端服務定義 ---
  backend:
    build: ./backend        # 指定使用 backend 資料夾內的 Dockerfile 建置映像檔
    container_name: dog-backend # 指定容器名稱，方便識別
    ports:
      - "8000:8000"         # 端口映射：宿主機 8000 -> 容器 8000
    volumes:
      - ./backend:/app      # 【關鍵】掛載 Volume：將宿主機的 backend 資料夾同步到容器內的 /app
    environment:
      - DEBUG=True          # 設定環境變數
    command: python manage.py runserver 0.0.0.0:8000 # 覆寫 Dockerfile 的 CMD，確保開發模式啟動

  # --- 前端服務定義 ---
  frontend:
    build: ./frontend       # 指定使用 frontend 資料夾內的 Dockerfile 建置映像檔
    container_name: dog-frontend
    ports:
      - "5173:5173"         # 端口映射：宿主機 5173 -> 容器 5173 (Vite 預設端口)
    volumes:
      - ./frontend:/app     # 【關鍵】掛載程式碼，實現熱重載 (Hot Reload)
      - /app/node_modules   # 【重要技巧】保留容器內的 node_modules，避免被宿主機空資料夾覆蓋
    depends_on:
      - backend             # 依賴設定：確保 backend 先啟動，frontend 再啟動
```

### 4.3 關鍵觀念：Volumes 掛載與熱重載

在開發階段，Volumes (磁碟區) 的設定至關重要。

* **問題**：若沒有設定 Volumes，每次修改程式碼後，都必須重新執行 `docker build` 才能將變更打包進映像檔，開發效率極低。
* **解決方案**：
* `./backend:/app`：這行指令建立了「雙向同步通道」。當開發者在 VS Code 修改了 `backend/views.py`，容器內的 `/app/views.py` 也會同時改變。
* **Hot Reload**：Django 的 `runserver` 與 Vite 的開發伺服器均具備檔案監控功能。一旦偵測到容器內的檔案變更，就會自動重啟服務或刷新頁面，達到與本機開發完全相同的體驗。



### 4.4 關鍵觀念：Docker Network 內部通訊

在 Docker Compose 中，所有定義的服務預設會加入同一個虛擬網路。這意味著容器之間可以透過 **服務名稱 (Service Name)** 互相溝通，而不需要知道對方的 IP 位址。

* **錯誤寫法**：前端呼叫後端時寫 `localhost:8000` (這在容器內會指向容器自己)。
* **正確觀念**：
* **瀏覽器 (宿主機)** 訪問前端：`localhost:5173`。
* **瀏覽器 (宿主機)** 訪問後端 API：`localhost:8000`。
* **容器間通訊** (例如後端容器要連資料庫容器)：應使用 `db:5432` (若有定義 db 服務)。



*(註：由於本專案是前後端分離架構，前端程式碼是在使用者的瀏覽器上執行，因此前端呼叫 API 時仍應指向 `localhost:8000`，因為瀏覽器位於宿主機網路環境中。)*
