from django.urls import reverse  # 用於反查 URL，避免在程式碼中寫死路徑 (如 '/api/dogs/')
from rest_framework import status  # 引入標準 HTTP 狀態碼常數，增加程式碼可讀性 (如 HTTP_200_OK)
from rest_framework.test import APITestCase  # DRF 提供的測試基類，內建了強大的測試客戶端 (APIClient)
from .models import DogImage  # 引入我們要測試的資料庫模型

class DogApiTests(APITestCase):
    """
    針對 DogImage API 的整合測試類別。
    繼承自 APITestCase，這意味著每次測試都會自動建立並銷毀一個獨立的測試資料庫，確保測試之間互不干擾。
    """
    
    def setUp(self):
        """
        [測試前的環境設定]
        這個方法會在「每一個」測試方法 (test_...) 執行之前自動執行一次。
        用來準備該次測試所需的基礎資料與變數。
        """
        # 1. 建立一筆測試用的初始資料
        # 定義資料內容 (模擬一筆收藏的圖片)
        self.dog_data = {'url': 'https://google.com/不存在的圖.jpg'}
        
        # 透過 Django ORM 在「測試專用的資料庫」中實際建立這筆資料。
        # 使用 **self.dog_data (字典解包) 將資料作為參數傳入 create 方法。
        self.dog = DogImage.objects.create(**self.dog_data)
        
        # 2. 設定正確的 API URL
        # 我們使用 reverse() 來反查 URL，而不是寫死字串，這樣就算未來網址規則改變，測試程式也不用修。
        
        # DRF 的 DefaultRouter 會自動根據 ViewSet 註冊名稱生成 URL pattern。
        # 預設規則為：'{model_name}-list' (對應列表頁) 與 '{model_name}-detail' (對應詳情頁)。
        
        # self.list_create_url 對應路徑：/api/dogs/ (用於 GET 列表與 POST 新增)
        self.list_create_url = reverse('dogimage-list')
        
        # self.detail_url 對應路徑：/api/dogs/{id}/ (用於 GET 單筆、PUT 修改、DELETE 刪除)
        # args=[self.dog.id] 會將剛剛建立的那筆資料 ID 自動填入 URL 中 (例如 /api/dogs/1/)。
        self.detail_url = reverse('dogimage-detail', args=[self.dog.id])

    # --- 測試 1: 取得收藏列表 (GET) ---
    def test_get_favorite_dogs(self):
        """
        測試情境：使用者發送 GET 請求到列表端點。
        預期結果：伺服器回傳 200 OK，且回傳的資料列表中包含我們在 setUp 建立的那筆資料。
        """
        # 使用測試客戶端 (self.client) 模擬瀏覽器發送 GET 請求
        response = self.client.get(self.list_create_url)
        
        # 斷言 (Assert) 1: 檢查 HTTP 狀態碼是否為 200 (成功)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 斷言 2: 檢查回傳的資料筆數是否正確 (setUp 建立了一筆，所以長度應為 1)
        # response.data 是 DRF 解析後的 JSON 資料 (Python 字典/列表格式)
        self.assertEqual(len(response.data), 1)
        
        # 斷言 3: 檢查回傳的內容細節
        # 確認第一筆資料 (index 0) 的 'url' 欄位是否與我們建立時的資料一致
        self.assertEqual(response.data[0]['url'], self.dog_data['url'])

    # --- 測試 2: 新增收藏 (POST) ---
    def test_create_favorite_dog(self):
        """
        測試情境：使用者發送 POST 請求並附帶 JSON 資料。
        預期結果：伺服器回傳 201 Created，測試專用資料庫中的總筆數增加，且新資料內容正確。
        """
        # 準備要新增的 Payload (請求內容)
        new_dog_data = {'url': 'https://google.com/不存在的圖.jpg'}
        
        # 發送 POST 請求
        # format='json' 告訴測試客戶端將資料序列化為 JSON 格式，並設定 Content-Type application/json
        response = self.client.post(self.list_create_url, new_dog_data, format='json')
        
        # 斷言 1: 建立資源成功的標準狀態碼應為 201 Created (而非 200)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 斷言 2: 檢查測試專用資料庫的狀態
        # 原本 setUp 有 1 筆，新增成功後應該變成 2 筆
        self.assertEqual(DogImage.objects.count(), 2) 
        
        # 斷言 3: 驗證資料正確性
        # 從 response 中拿到新建立物件的 ID，再從資料庫撈出來比對 URL 是否正確寫入
        self.assertEqual(DogImage.objects.get(id=response.data['id']).url, new_dog_data['url'])

    # --- 測試 3: 刪除收藏 (DELETE) ---
    def test_delete_favorite_dog(self):
        """
        測試情境：使用者針對特定 ID 發送 DELETE 請求。
        預期結果：伺服器回傳 204 No Content，且資料庫中該筆資料確實被移除。
        """
        # 發送 DELETE 請求到詳情頁面 (針對 setUp 建立的那筆 dog)
        response = self.client.delete(self.detail_url)
        
        # 斷言 1: 刪除成功的標準狀態碼應為 204 No Content
        # 204 代表請求成功處理，但回應本體 (Body) 不包含任何內容
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # 斷言 2: 檢查資料庫狀態
        # 唯一的資料被刪除後，資料庫應該要是空的 (count 為 0)
        self.assertEqual(DogImage.objects.count(), 0)