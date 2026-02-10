# Django ORM 與模型設計

## 第一章：Django ORM 基礎概念

### 什麼是 ORM？
ORM 代表 Object-Relational Mapping（物件關聯映射），是一種將資料庫表格與 Python 類別相互映射的技術。

**核心優勢：**
- 無需直接編寫 SQL，用 Python 物件操作資料庫
- 自動處理資料庫差異，提高代碼可移植性
- 內建安全機制，防止 SQL 注入攻擊
- 便於資料驗證和業務邏輯整合

### ORM 工作流程
```
Python Model 類別 → Django ORM → SQL 語句 → 資料庫
資料庫結果 → 模型實例 → Python 物件操作 → JSON 回應
```

---

## 第二章：Django Models 模型定義

### 模型的基本結構
```python
from django.db import models

class DogImage(models.Model):
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dog Image {self.id}"
```

### 欄位類型詳解

| 欄位類型 | 用途 | 特點 |
|---------|------|------|
| `CharField` | 短文本 | 需指定 `max_length` |
| `TextField` | 長文本 | 無長度限制 |
| `URLField` | 網址 | 內建 URL 格式驗證 |
| `IntegerField` | 整數 | 存儲數字 |
| `DateTimeField` | 日期時間 | 並支援自動時間戳 |
| `BooleanField` | 布林值 | 真/假 |
| `ForeignKey` | 外鍵 | 建立關聯關係 |

### 欄位參數詳解

**常用參數說明：**
- `auto_now_add=True`：建立記錄時自動設置當前時間，之後不再改變
- `auto_now=True`：每次儲存都更新為當前時間
- `max_length`：最大字元數（CharField 和 URLField 必需）
- `null=True`：允許 NULL 值（資料庫層級）
- `blank=True`：表單驗證時允許空白（表單層級）
- `default`：設置預設值

---

## 第三章：資料庫遷移 (Migration)

### 遷移的作用
遷移是追蹤模型變更並應用到資料庫的機制。

**兩個關鍵命令：**

1. **makemigrations**：偵測模型變化，產生遷移檔
   ```bash
   python manage.py makemigrations
   ```
   - Django 掃描所有 App 的 models.py
   - 比較與上一版本的差異
   - 在 `migrations/` 資料夾生成遷移檔

2. **migrate**：將遷移檔應用到資料庫
   ```bash
   python manage.py migrate
   ```
   - 按順序執行遷移檔中的 SQL 語句
   - 更新資料庫 Schema
   - 記錄已應用的遷移版本

### 遷移檔的含義
遷移檔中包含 `operations` 列表，定義了要執行的資料庫操作：
- `CreateModel`：建立新表格
- `AddField`：新增欄位
- `RemoveField`：移除欄位
- `AlterField`：修改欄位特性

---

## 第四章：__str__ 方法與模型表達

### 定義模型的字串表達
```python
def __str__(self):
    return f"Dog Image {self.id}"
```

**用途：**
1. Django Admin 後台顯示時會調用此方法
2. 在 Python REPL 或日誌中列印模型實例時更易讀
3. 提升開發除錯效率

**最佳實踐：**
```python
def __str__(self):
    # 包含有意義的識別資訊
    return f"{self.name} (ID: {self.id})"
```

---

## 第五章：QuerySet 與資料查詢

### QuerySet 基本操作

**取得所有資料：**
```python
DogImage.objects.all()
```

**排序資料：**
```python
# 升序（預設）
DogImage.objects.all().order_by('created_at')

# 降序（前綴加負號）
DogImage.objects.all().order_by('-created_at')
```

**篩選資料：**
```python
# 單條件篩選
DogImage.objects.filter(id=5)

# 多條件篩選（AND）
DogImage.objects.filter(id=5, url='...')

# 排除篩選
DogImage.objects.exclude(id=5)
```

**聚合與統計：**
```python
DogImage.objects.count()  # 計數
DogImage.objects.exists()  # 檢查是否存在
```

### 鏈式調用（Method Chaining）
```python
# 組合多個操作
DogImage.objects
    .filter(created_at__gte='2024-01-01')  # 大於等於
    .order_by('-created_at')  # 降序排列
    .distinct()  # 去重
    .values('url')  # 只取 url 欄位
```

---

## 第六章：模型關係設計

### 一對多關係 (One-to-Many)
```python
class User(models.Model):
    name = models.CharField(max_length=100)

class DogImage(models.Model):
    url = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```
在一個模型（如 `DogImage`）中定義 `ForeignKey` 指向另一個模型（如 `User`）時，Django 會自動在目標模型（`User`）的實例上新增一個屬性，其預設命名格式為： **`子模型類別名稱的小寫` + `_set`** (如 user.dogimage_set.all())


**on_delete 參數詳解：**
- `models.CASCADE`：父資料刪除時，子資料也刪除
- `models.SET_NULL`：父資料刪除時，子資料設為 NULL（需 `null=True`）
- `models.PROTECT`：禁止刪除有子資料的父資料
- `models.SET_DEFAULT`：設為預設值

### 反向關係查詢
```python
# 取得某個使用者的所有狗狗圖片
user = User.objects.get(id=1)
user.dogimage_set.all()  # 自動複數形式
```

---

## 總結

Django ORM 提供：
✅ 強大的資料庫抽象層
✅ 自動遷移管理
✅ 靈活的查詢 API
✅ 內建安全驗證
✅ 物件導向的資料操作方式
