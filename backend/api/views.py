""" 
這段程式碼採用了 DRF ViewSet，是 Django REST Framework 中最高效且具備高度封裝性的視圖邏輯。

1.自動化 CRUD 邏輯：繼承 viewsets.ModelViewSet 後，系統會自動處理標準的增、刪、查、改（Create, Retrieve, Update, Delete）行為，無需手動撰寫 get() 或 post() 方法。
2.資料集控管 (queryset)：定義了 API 存取的原始資料來源。使用 .order_by('-created_at') 確保回傳結果符合「最新優先」的邏輯，常見於動態牆或收藏列表。
3.宣告式關聯：透過 serializer_class 綁定先前的序列化器，讓 ViewSet 知道如何處理資料的輸入驗證與輸出轉換。
"""

from django.shortcuts import render
from rest_framework import viewsets
from .models import DogImage
from .serializers import DogImageSerializer

# 使用 ModelViewSet 自動封裝所有標準的 API 動作 (List, Create, Retrieve, Update, Destroy)
class DogImageViewSet(viewsets.ModelViewSet):
    # 定義要從資料庫提取的資料範圍，並依建立時間「降冪」排列 (由新到舊)
    # 下面出現 DogImage，這是在 models.py 中定義的 Django Model，代表資料庫中的一個資料表。
    queryset = DogImage.objects.all().order_by('-created_at')

    # 指定這個 ViewSet 使用哪個 Serializer 來處理資料的驗證與轉換。
    serializer_class = DogImageSerializer
