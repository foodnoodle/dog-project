"""  
這段程式碼負責配置 API 路由系統，利用 DRF 的路由器（Router）自動化管理路徑。

自動化路徑映射：DefaultRouter 會自動分析 DogImageViewSet 的動作，生成對應的 RESTful 網址，例如：
1. GET /dogs/ (取得清單)
2. POST /dogs/ (新增資料)
3. GET /dogs/{id}/ (取得單筆資料)

標準化介面：相較於手動撰寫 path()，使用 Router 能確保 API 的 URL 結構符合 REST 慣例，減少人為錯誤。
API 根索引：DefaultRouter 會額外提供一個自動生成的 API Root 頁面，方便開發者在瀏覽器中直接查看並測試所有已註冊的介面。
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DogImageViewSet

# 初始化一個 DRF 的路由器 (Router)，用於自動生成 API 路由。
router = DefaultRouter()

# 註冊路由器
# r'dogs'：這是網址的前綴 (URL Prefix)
# DogImageViewSet：這是處理邏輯的集合點
router.register(r'dogs', DogImageViewSet)

# 最終對應結果：
# 前端呼叫 GET /dogs/  => 觸發 DogImageViewSet.list()
# 前端呼叫 GET /dogs/5/ => 觸發 DogImageViewSet.retrieve() (取得 ID 為 5 的資料)
# 只需定義一個「前綴」，Router 就會把整套增刪查改的「路徑網」全部鋪設完成。

# 將路由器生成的網址清單整合進 Django 的路徑配置中
urlpatterns = [
    # include(router.urls) 會自動引入多組路由（如 list, create, detail 等）
    path('',include(router.urls)),
]