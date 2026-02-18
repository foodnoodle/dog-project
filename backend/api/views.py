""" 
這段程式碼採用了 DRF ViewSet，是 Django REST Framework 中最高效且具備高度封裝性的視圖邏輯。

1.自動化 CRUD 邏輯：繼承 viewsets.ModelViewSet 後，系統會自動處理標準的增、刪、查、改（Create, Retrieve, Update, Delete）行為，無需手動撰寫 get() 或 post() 方法。
2.資料集控管 (queryset)：定義了 API 存取的原始資料來源。使用 .order_by('-created_at') 確保回傳結果符合「最新優先」的邏輯，常見於動態牆或收藏列表。
3.宣告式關聯：透過 serializer_class 綁定先前的序列化器，讓 ViewSet 知道如何處理資料的輸入驗證與輸出轉換。
"""
from rest_framework import viewsets, permissions  # 新增 permissions
from django.shortcuts import render
from rest_framework import viewsets
from .models import DogImage
from .serializers import DogImageSerializer
# 匯入 drf-spectacular 的文件工具
from drf_spectacular.utils import extend_schema, extend_schema_view

# 使用裝飾器為 ViewSet 的各種動作添加「中文說明」，貼在目標函式的頭上即可
@extend_schema_view(
    # list: 對應 GET /api/dogs/ (取得清單)
    list=extend_schema(
        summary="取得圖片收藏列表",
        description="回傳所有已收藏的狗狗圖片資料。列表會依照建立時間由新到舊排序，最新的在最上面。"
    ),
    # create: 對應 POST /api/dogs/ (新增)
    create=extend_schema(
        summary="收藏新的圖片",
        description="將一張新的狗狗圖片網址 (URL) 加入到資料庫中。"
    ),
    # retrieve: 對應 GET /api/dogs/{id}/ (取得單筆) - 就是您剛剛測試的那個
    retrieve=extend_schema(
        summary="查看單筆圖片資訊",
        description="根據 ID 取得特定一張收藏圖片的詳細資料（包含 ID、圖片網址、收藏時間）。"
    ),
    # update: 對應 PUT /api/dogs/{id}/ (完整修改)
    update=extend_schema(
        summary="修改圖片資訊 (完整)",
        description="更新特定收藏的內容。"
    ),
    # partial_update: 對應 PATCH /api/dogs/{id}/ (部分修改)
    partial_update=extend_schema(
        summary="修改圖片資訊 (部分)",
        description="更新特定收藏的部分內容。"
    ),
    # destroy: 對應 DELETE /api/dogs/{id}/ (刪除)
    destroy=extend_schema(
        summary="移除收藏",
        description="將這張圖片從您的收藏資料庫中永久刪除。"
    )
)
# 使用 ModelViewSet 自動封裝所有標準的 API 動作 (List, Create, Retrieve, Update, Destroy)
class DogImageViewSet(viewsets.ModelViewSet):
    # 定義要從資料庫提取的資料範圍，並依建立時間「降冪」排列 (由新到舊)
    # 下面出現 DogImage，這是在 models.py 中定義的 Django Model，代表資料庫中的一個資料表。
    queryset = DogImage.objects.all().order_by('-created_at')

    # 指定這個 ViewSet 使用哪個 Serializer 來處理資料的驗證與轉換。
    serializer_class = DogImageSerializer

    # 1. 加上警衛：只有登入的使用者才能存取
    permission_classes = [permissions.IsAuthenticated]

    # 2. 過濾視野：只回傳「我是主人」的圖片
    def get_queryset(self):
        return DogImage.objects.filter(owner=self.request.user).order_by('-created_at')

    # 3. 自動標記：存檔時，自動把 owner 填成目前登入的使用者
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)