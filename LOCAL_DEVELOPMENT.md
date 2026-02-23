## 🖥️ 本地開發環境建置 (Local Development Setup)

若您偏好在宿主機直接進行開發而非使用 Docker 容器，請遵循以下配置說明：

### 1. Python 後端環境 (使用 uv)

本專案採用 **uv** 作為現代化的 Python 套件管理工具，以確保依賴項的高速安裝與版本一致性。

* **安裝 uv**：
* **Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

* **macOS / Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* **同步虛擬環境**：
進入後端目錄並執行同步指令，此動作會自動建立 `.venv` 並安裝所有必要套件：
```bash
cd backend
uv sync
```

* **VS Code 解譯器選取 (Interpreter Selection)**：
1. 於 VS Code 按下 `Ctrl + Shift + P` (或 `Cmd + Shift + P`) 開啟指令面板。
2. 輸入並選取 **`Python: Select Interpreter`**。
3. 手動指向專案內的虛擬環境路徑：
* **Windows**: `./backend/.venv/Scripts/python.exe`
* **macOS / Linux**: `./backend/.venv/bin/python`

### 2. Vue 前端環境 (使用 npm)

前端開發依賴於 Node.js 環境，請確保您的系統已安裝相應版本。

* **安裝相依套件**：
進入前端目錄並執行安裝指令：
```bash
cd frontend
npm install
```

* **啟動開發伺服器**：
執行以下指令開啟具備熱重載功能的 Vite 服務：
```bash
npm run dev
```
