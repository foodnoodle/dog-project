# 狗狗收藏館 (Dog Image Collection) 🐕

這是一個採用前後端分離架構開發的全棧應用程式，使用者可以瀏覽隨機生成的狗狗圖片，並將心儀的圖片收藏至個人資料庫中。

## 🚀 技術棧 (Tech Stack)

### 🐍 後端技術 (Backend)

* **執行環境**: **Python 3.14**
* **Web 框架**: **Django 6.0.2**，負責處理後端邏輯與資料庫互動。
* **API 框架**: **Django REST Framework (DRF) 3.16.1**，用於構建 RESTful API 介面，並透過 `ModelViewSet` 與 `DefaultRouter` 實現自動化路由與 CRUD 功能。
* **套件管理**: 使用 **uv** 作為現代化的 Python 套件管理與虛擬環境建置工具。
* **跨網域處理**: 透過 **django-cors-headers** 解決前後端分離產生的 CORS (跨網域資源共享) 問題。
* **資料庫**: 使用 **SQLite3**，用於儲存圖片網址 (URL) 與建立時間戳記。

### ⚡ 前端技術 (Frontend)

* **開發框架**: **Vue 3**，採用 **SFC (Single File Components)** 與 **Composition API (`<script setup>`)** 模式開發。
* **構建工具**: **Vite 7.2.4**，提供極速的開發環境熱重載與優化的生產環境打包。
* **前端路由**: **Vue Router 4.6.4**，管理「首頁」與「收藏頁」之間的視圖切換。
* **HTTP 客戶端**: **Axios 1.13.4**，負責與外部 Dog CEO API 溝通獲取隨機圖片，並與自定義的 Django 後端 API 進行資料同步。

## 🛠️ 開發工具與視覺化

<table width="100%">
  <thead>
    <tr>
      <th width="50%">Git 版本控制 (VS Code Source Control)</th>
      <th width="50%">資料庫視覺化管理 (SQLite Viewer)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">
        <img src="images/git_source_control.png" height="350">
      </td>
      <td align="center">
        <img src="images/sqlite_viewer.png" height="350">
      </td>
    </tr>
    <tr>
      <td>使用 VS Code 內建的 Source Control 功能進行版本控制，包含檔案變更追蹤、暫存 (stage) 與提交 (commit)。</td>
      <td>透過 SQLite Viewer 開啟資料庫檔案，瀏覽資料表結構與內容，確認資料正確性。</td>
    </tr>
  </tbody>
</table>


## 🌟 核心功能

1. **隨機狗狗抽卡 (HomeView)**:

<img src="https://github.com/user-attachments/assets/b60d6b4e-9a6c-4cde-801e-58ff773a30c1" width="500" alt="隨機抽卡">
       
* 從外部 Dog CEO API 獲取即時的隨機狗狗圖片。
  
<img src="https://github.com/user-attachments/assets/d8deb2b4-bd50-4e6a-907b-9c0c24a0f3f9" width="500" alt="隨機抽卡">
  
* 提供「收藏這張」功能，透過 `POST` 請求將圖片網址傳送至後端儲存。

2. **我的收藏庫 (FavoritesView)**:
   
<img src="https://github.com/user-attachments/assets/fa4a40cd-e1aa-48e0-9cbc-7f61125261c3" width="500" alt="隨機抽卡">
 
* 展示所有儲存於資料庫中的狗狗圖片，預設依據建立時間進行降冪排列（最新收藏的排在最前）。
* 提供「刪除」功能，可直接從後端資料庫移除指定的收藏項目。


3. **響應式網格佈局**:
* 收藏列表具備響應式設計，能在不同裝置螢幕下自動調整圖片排列順序。


## 📂 專案結構

* **`backend/`**: 包含 Django 的核心配置 (`config/`) 以及 API 應用程式 (`api/`)，定義了 `DogImage` 模型與序列化邏輯。
* **`frontend/`**: 包含 Vue 應用程式，主要組件位於 `src/components/` (如 `RandomDog.vue`, `FavoriteList.vue`)。

## 🔗 API 端點 (Django)

* `GET /api/dogs/`: 獲取收藏清單。
* `POST /api/dogs/`: 新增一張狗狗圖片至收藏。
* `DELETE /api/dogs/{id}/`: 根據 ID 移除收藏。
