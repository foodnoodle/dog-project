"""
這是用來檢查 docker 容器內的環境變數和模型清單
"""
import os
import google.generativeai as genai

# 讀取容器內的環境變數
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print(f"使用的 API Key 前五碼: {api_key[:5] if api_key else '未找到'}")
print("=== 支援 generateContent 的模型清單 ===")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"查詢失敗: {e}")