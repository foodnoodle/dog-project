# Django REST Framework API 設計

## 第一章：RESTful API 基礎

### REST 原則
REST (Representational State Transfer) 是設計 Web API 的架構風格。

**核心原則：**
1. **資源導向**：用名詞表示資源（不是動詞）
   - ✅ `/dogs/` 而非 `/getDogs/`
   
2. **HTTP 方法對應操作**：
   - `GET`：取得資料
   - `POST`：建立資料
   - `PUT/PATCH`：更新資料
   - `DELETE`：刪除資料

3. **無狀態設計**：每個請求包含完整信息，伺服器不保存客戶端上下文

4. **統一介面**：
   - 標準的 HTTP 狀態碼
   - JSON 格式的資料交換
   - 可預測的 URL 結構

### REST API 範例表格

| 操作 | 方法 | URL | 說明 |
|------|------|-----|------|
| 列表 | GET | `/dogs/` | 取得所有狗狗圖片 |
| 建立 | POST | `/dogs/` | 新增一筆狗狗圖片 |
| 詳細 | GET | `/dogs/5/` | 取得 ID 為 5 的狗狗圖片 |
| 更新 | PUT | `/dogs/5/` | 完全更新（所有欄位） |
| 部分更新 | PATCH | `/dogs/5/` | 部分更新（指定欄位） |
| 刪除 | DELETE | `/dogs/5/` | 刪除 ID 為 5 的狗狗圖片 |

---

## 第二章：Serializers 序列化器

### 序列化器的角色
Serializer 是 DRF 中最重要的元件，承擔三個角色：

1. **資料轉換**：Model 實例 ↔ JSON
2. **驗證**：確保輸入資料符合規範
3. **反序列化**：JSON → Model 實例

### ModelSerializer 的自動化映射

```python
from rest_framework import serializers
from .models import DogImage

class DogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogImage
        fields = '__all__'  # 轉換所有欄位
```

**自動化映射的機制：**

當 DRF 讀取 `DogImage` Model，會自動生成以下序列化器欄位：

| Model 欄位 | 自動對應的 Serializer 欄位 | 特性 |
|-----------|------------------------|------|
| `URLField` | `serializers.URLField` | 自動驗證 URL 格式 |
| `DateTimeField` | `serializers.DateTimeField` | ISO 8601 格式的日期 |
| Auto-generated `id` | `serializers.IntegerField` | 唯讀，由資料庫自動生成 |

### 選擇性欄位映射

```python
class DogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogImage
        fields = ['id', 'url', 'created_at']  # 明確指定欄位
        # fields = ('id', 'url')  # 也可用元組
```

### 自訂序列化器欄位

```python
class DogImageSerializer(serializers.ModelSerializer):
    # 新增讀寫分離的欄位
    created_at_display = serializers.SerializerMethodField()
    
    class Meta:
        model = DogImage
        fields = '__all__'
    
    def get_created_at_display(self, obj):
        # 自訂日期格式
        return obj.created_at.strftime('%Y年%m月%d日')
```

---

## 第三章：ViewSet 與自動化 CRUD

### ModelViewSet 的強大功能

```python
from rest_framework import viewsets
from .models import DogImage
from .serializers import DogImageSerializer

class DogImageViewSet(viewsets.ModelViewSet):
    queryset = DogImage.objects.all().order_by('-created_at')
    serializer_class = DogImageSerializer
```

**一個 ViewSet 可以自動提供以下方法：**

| 方法 | HTTP 動詞 | URL | 功能 |
|------|---------|-----|------|
| `list()` | GET | `/dogs/` | 列出所有資料 |
| `create()` | POST | `/dogs/` | 新建資料 |
| `retrieve()` | GET | `/dogs/{id}/` | 取得單筆資料 |
| `update()` | PUT | `/dogs/{id}/` | 完全更新 |
| `partial_update()` | PATCH | `/dogs/{id}/` | 部分更新 |
| `destroy()` | DELETE | `/dogs/{id}/` | 刪除資料 |

### QuerySet 的重要性

```python
# ✅ 好的範例：排序最新優先
queryset = DogImage.objects.all().order_by('-created_at')

# ⚠️ 避免：不排序可能導致不可預測的順序
# queryset = DogImage.objects.all()
```

**為什麼排序很重要：**
- 使 API 行為可預測
- 提升使用者體驗（最新內容優先）
- 避免資料庫性能問題（大量資料時無序查詢很慢）

---

## 第四章：DRF 路由系統

### DefaultRouter 自動路由生成

```python
from rest_framework.routers import DefaultRouter
from .views import DogImageViewSet

router = DefaultRouter()
router.register(r'dogs', DogImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

**Router 生成的完整路由：**
```
GET    /dogs/                     → 列表視圖
POST   /dogs/                     → 建立視圖
GET    /dogs/{id}/                → 詳細視圖
PUT    /dogs/{id}/                → 更新視圖
PATCH  /dogs/{id}/                → 部分更新視圖
DELETE /dogs/{id}/                → 刪除視圖
GET    /                          → API 根頁面（自動生成）
```

### Router 的自動化優勢

1. **一致性**：所有 API 端點遵循 REST 慣例
2. **可發現性**：API 根頁面提供所有可用端點清單
3. **省力**：無需手動編寫每個路由

---

## 第五章：HTTP 狀態碼與回應

### 常見的 HTTP 狀態碼

**成功類（2xx）：**
- `200 OK`：成功取得資料
- `201 Created`：資源成功建立
- `204 No Content`：成功刪除或更新（無回應體）

**客戶端錯誤（4xx）：**
- `400 Bad Request`：請求格式錯誤
- `404 Not Found`：資源不存在
- `405 Method Not Allowed`：HTTP 方法不允許

**伺服器錯誤（5xx）：**
- `500 Internal Server Error`：伺服器內部錯誤
- `503 Service Unavailable`：伺服器不可用

### DRF 自動狀態碼映射

```python
# POST 成功時自動返回 201
response → 201 Created + JSON 資料

# DELETE 成功時自動返回 204
response → 204 No Content

# 驗證失敗時自動返回 400
error → 400 Bad Request + 錯誤訊息
```

---

## 第六章：資料驗證

### 序列化器內建驗證

```python
class DogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogImage
        fields = '__all__'
    
    def validate_url(self, value):
        # 自訂欄位驗證
        if not value.startswith('http'):
            raise serializers.ValidationError(
                "URL 必須以 http 或 https 開頭"
            )
        return value
```

**驗證層級：**
1. 欄位級驗證（Field-level）：單個欄位的驗證
2. 物件級驗證（Object-level）：多欄位間的關聯驗證

### 常見驗證規則

| 驗證類型 | 說明 | 用例 |
|---------|------|------|
| 格式驗證 | URLField 自動驗證 | 檢查是否為有效 URL |
| 長度驗證 | max_length | URLField(max_length=500) |
| 類型驗證 | 欄位型別 | IntegerField 不接受字符串 |
| 唯一性 | unique=True | 防止重複資料 |

---

## 總結

Django REST Framework 提供：
✅ 自動化 CRUD 操作（ViewSet）
✅ 靈活的資料轉換（Serializers）
✅ 符合 REST 標準的 API 設計
✅ 內建驗證與錯誤處理
✅ 強大的路由系統
✅ 可瀏覽的 API 介面
