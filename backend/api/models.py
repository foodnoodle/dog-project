""" 
makemigrations：
全域偵測 Django 會掃描 INSTALLED_APPS 中註冊的所有資料夾，
尋找每個 App 下的 models.py。

migrate：
按序同步 將所有 App 的遷移檔轉換為 SQL 語法，並實際套用到資料庫。

"""
# 這段程式碼定義了 Django Model(模型)，
# 用於表示和操作資料庫結構(Schema)中的 DogImage(狗狗圖片) 資料表。
from django.db import models

""" 
DRF 讀取到 Model 名稱是 DogImage，
它會自動將駝峰式命名（CamelCase）拆開變成 "Dog Image"，
並且因為您現在位於「列表頁面」（可以看到所有資料的地方），
所以它自動加上了 "List"。
"""
class DogImage(models.Model):
    # 儲存圖片的網址，內建格式驗證，長度上限 500 字元
    url = models.URLField(max_length=500)

    # 自動記錄圖片資料建立的時間戳記。
    created_at = models.DateTimeField(auto_now_add=True)

    # 定義物件的字串表達形式(有利於 Django Admin 後台顯示)。
    def __str__(self):
        return f"Dog Image {self.id}"