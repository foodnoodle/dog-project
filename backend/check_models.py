"""
這是用來檢查 docker 容器內的環境變數和模型清單
"""
import os
from google import genai

# 讀取容器內的環境變數
api_key = os.environ.get("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    print(f"使用的 API Key 前五碼: {api_key[:5] if api_key else '未找到'}")
    print("=== 支援 generateContent 的模型清單 (部分列出) ===")
    
    # 新版 SDK 的 list_models 用法可能不同，這裡嘗試列出
    # 注意: google-genai SDK 目前可能沒有直接對應老版 list_models 的簡單方法，
    # 或者需要查閱文獻。這裡我們先嘗試用 client.models.list()
    
    for m in client.models.list():
        # 過濾出支援 generateContent 的模型 (新版 SDK 模型物件屬性可能因版本而異)
        # 這裡簡單印出所有模型名稱
        print(f"- {m.name}")

except Exception as e:
    print(f"查詢失敗: {e}")