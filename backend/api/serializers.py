""" 
這段程式碼定義了 DRF (Django Rest Framework) Serializer，它是 Django 模型與前端 JSON 數據之間的「橋樑」。

1.資料轉換器：其核心功能是將複雜的資料庫物件（QuerySet/Model instances）轉換成 Python 原生資料型別，隨後即可輕鬆渲染成 JSON 格式。
2.自動化映射：繼承 ModelSerializer 後，DRF 會自動讀取 DogImage 的欄位定義，並根據模型屬性（如 URLField）自動生成相應的資料驗證邏輯。
3.Meta 類別作用：透過 class Meta 進行配置，明確指定序列化的「對象（model）」與「範圍（fields）」，實現宣告式開發，大幅減少手動撰寫欄位代碼。
"""
from rest_framework import serializers
from .models import DogImage

class DogImageSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定要關聯的資料庫模型
        model = DogImage
        # 轉換所有欄位 (id, url, created_at)
        fields = '__all__'