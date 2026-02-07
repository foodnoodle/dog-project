## 第二章：Docker 三大核心組件

### 2.1 核心架構概覽

Docker 的運作體系由三個核心元件組成：**映像檔 (Image)**、**容器 (Container)** 與 **倉庫 (Repository)**。這三者的關係可類比於物件導向程式設計 (OOP) 中的「類別」與「物件」。

| Docker 組件 | 程式設計類比 | 功能定義 |
| --- | --- | --- |
| **Image (映像檔)** | **Class (類別)** | 靜態的應用程式藍圖，包含程式碼、執行環境與系統函式庫。 |
| **Container (容器)** | **Object (物件)** | 映像檔執行後的動態實例 (Instance)。 |
| **Repository (倉庫)** | **Package Manager** | 集中存放與版本管理映像檔的伺服器 (如 Docker Hub)。 |

### 2.2 映像檔 (Image)：靜態的唯讀藍圖

映像檔是一個**唯讀 (Read-only)** 的模板。它透過分層儲存 (Layered Storage) 的方式，將作業系統基底、語言環境與應用程式碼堆疊在一起。

**在 `dog-project` 中的應用：**
專案中的 `backend/Dockerfile` 即是製作後端映像檔的「食譜」。當建置 (Build) 完成後，會產生一個包含以下內容的 Image：

1. **Base Layer**：Linux 作業系統 (如 `python:3.9-slim`)。
2. **Dependency Layer**：安裝 Django、DRF 等 Python 套件。
3. **App Layer**：`dog-project` 的後端程式碼 (`api/`, `config/`, `manage.py`)。

一旦建立完成，這個 Image 的內容即固定不變，確保了部署環境的一致性。

### 2.3 容器 (Container)：執行的動態實例

容器是映像檔**執行時 (Runtime)** 的實體。當 Docker 啟動一個 Image 時，會在該 Image 的最上層掛載一個**可讀寫層 (Writable Layer)**。

**運作機制：**

* **隔離執行**：每個容器擁有獨立的 Process 空間、網路介面與檔案系統。
* **生命週期**：容器可以被建立、啟動、停止或刪除。
* **資料特性**：在容器運作期間產生的檔案變更（例如：Django 產生的 `__pycache__` 或日誌檔），皆儲存於可讀寫層。**若刪除容器，該層資料將隨之消失**。這也是為何資料庫檔案 (`db.sqlite3`) 通常需要透過 Volume 掛載到宿主機的原因。

**在 `dog-project` 中的應用：**
執行 `docker-compose up` 後，系統會分別啟動：

1. 一個運行 Django API 的後端容器。
2. 一個運行 Vite 開發伺服器的前端容器。
兩者雖由不同 Image 建立，但可透過 Docker Network 互相通訊。

### 2.4 倉庫 (Repository)：映像檔的集散地

倉庫是用於存放與分享映像檔的雲端服務。

* **Docker Hub**：官方的公開倉庫。
* **運作流程**：
1. 當 `Dockerfile` 中指定 `FROM python:3.9` 時，Docker Daemon 會先檢查本地端是否有該映像檔。
2. 若無，則自動從 Docker Hub 下載 (Pull) 該基礎映像檔到本地。
