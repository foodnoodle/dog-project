## 第五章：常用指令工具手冊 (Cheat Sheet)

### 5.1 Docker Compose 專用指令 (專案開發首選)

由於 `dog-project` 已經設定了 `docker-compose.yaml`，因此 90% 的開發情境應優先使用以下指令，而非單獨操作個別容器。

| 情境             | 指令                             | 說明                                                        |
| ---------------- | -------------------------------- | ----------------------------------------------------------- |
| **啟動專案**     | `docker-compose up`              | 啟動所有服務並在終端機顯示 Log (按 Ctrl+C 停止)。           |
| **背景啟動**     | `docker-compose up -d`           | 在背景啟動所有服務 (Detached mode)，不會佔用終端機。        |
| **停止並移除**   | `docker-compose down`            | 停止容器並**移除**它們 (網路也會移除，但 Volume 預設保留)。 |
| **查看日誌**     | `docker-compose logs -f`         | 持續追蹤 (Follow) 所有服務的輸出日誌。                      |
| **查看特定日誌** | `docker-compose logs -f backend` | 只追蹤後端服務的日誌。                                      |
| **重新建置**     | `docker-compose up --build`      | 當 Dockerfile 修改後，強制重新 Build 映像檔並啟動。         |

### 5.2 容器管理與除錯 (Container Operations)

當服務發生異常（例如 Django 報錯但容器沒死，或是需要進入容器內手動執行 `migrate`）時，需使用以下指令。

* **查看運行中的容器**
```bash
docker ps
# 若要包含已停止的容器，加上 -a
docker ps -a
```


* **進入容器內部 (Shell Access)**
這是在除錯時最重要的指令。
```bash
# 進入後端 (Debian/Ubuntu 基底通常有 bash)
docker exec -it dog-backend bash

# 進入前端 (Alpine 基底通常只有 sh)
docker exec -it dog-frontend sh
```

*(進入後，可以像在一般 Linux 環境下執行 `ls`, `cat`, 或 `python manage.py migrate`)*
* **手動停止/啟動單一容器**
```bash
docker stop dog-backend
docker start dog-backend
docker restart dog-backend
```

### 5.3 映像檔與清理 (Images & Cleanup)

隨著開發時間拉長，電腦中會堆積大量舊的 Image 與 Cache，定期清理是必要的。

* **列出所有映像檔**
```bash
docker images
```

* **刪除特定映像檔**
```bash
# 需先刪除使用該 Image 的容器才能刪除 Image
docker rmi <IMAGE_ID>
```
* **系統大掃除 (Prune)**
這是一個強大但需謹慎使用的指令。它會刪除所有「停止的容器」、「未被使用的網路」以及「懸空 (Dangling) 的映像檔」。
```bash
docker system prune
# 若要連同未使用的 Volume 一起刪除 (注意資料會遺失！)
docker system prune --volumes
```

### 5.4 實戰場景：資料庫遷移 (Migration)

在 Docker 環境下執行 Django Migration 的標準流程：

1. 確保後端容器正在運行：
`docker-compose up -d backend`
2. 進入後端容器：
`docker exec -it dog-backend bash`
3. 在容器內執行遷移指令：
```bash
python manage.py makemigrations
python manage.py migrate
```


4. 退出容器：
`exit`
