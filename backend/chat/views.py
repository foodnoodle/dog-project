import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatInputSerializer, ChatSessionListSerializer

# 引入全新世代的 Google SDK
from google import genai
from google.genai import types, errors

class ChatView(APIView):
    """
    狗狗 AI 對話介面
    提供針對狗狗圖片的發問、歷史紀錄獲取與清空功能。
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        獲取對話紀錄
        - 若提供 image_url: 回傳該圖片的詳細對話紀錄。
        - 若未提供 image_url: 回傳使用者的「所有」對話階段列表 (List)。
        """
        image_url = request.query_params.get('image_url')

        if image_url:
            # 有指定圖片 -> 獲取單一對話詳情
            session, _ = ChatSession.objects.get_or_create(user=request.user, image_url=image_url)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        else:
            # 未指定圖片 -> 獲取對話列表
            # 過濾掉沒有任何訊息的空 Session
            sessions = ChatSession.objects.filter(user=request.user, messages__isnull=False).distinct()
            serializer = ChatSessionListSerializer(sessions, many=True)
            return Response(serializer.data)

    @extend_schema(
        request=ChatInputSerializer, 
        responses={201: ChatSessionSerializer},
        description="傳送狗狗圖片網址與問題，獲取 AI 的多模態回覆"
    )
    def post(self, request):
        """針對狗狗圖片進行 AI 多模態發問 (Gemini 2.5 Flash)"""
        import logging
        logger = logging.getLogger(__name__)

        try:
            image_url = request.data.get('image_url')
            prompt = request.data.get('prompt')

            if not image_url or not prompt:
                return Response({"error": "缺少 image_url 或 prompt"}, status=status.HTTP_400_BAD_REQUEST)

            # 1. 獲取 Session
            session, _ = ChatSession.objects.get_or_create(user=request.user, image_url=image_url)

            # 2. 準備新版 SDK 要求的歷史紀錄格式 (types.Content)
            history_messages = session.messages.all().order_by('created_at')
            gemini_history = []
            for msg in history_messages:
                gemini_history.append(
                    types.Content(
                        role="user" if msg.role == "user" else "model",
                        parts=[types.Part.from_text(text=msg.content)]
                    )
                )

            # 3. 下載圖片
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            # 新版 SDK 處理圖片二進位的專屬寫法
            img_part = types.Part.from_bytes(
                data=img_response.content, 
                mime_type='image/jpeg'
            )

            # 4. 初始化新版客戶端與建立對話，並指定最新版的模型
            client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
            chat = client.chats.create(
                model='gemini-2.5-flash',
                history=gemini_history
            )
            
            # 5. 發送文字與圖片多模態陣列
            ai_response = chat.send_message([prompt, img_part])
            ai_text = ai_response.text

            # 6. 永久化儲存
            ChatMessage.objects.create(session=session, role='user', content=prompt)
            ChatMessage.objects.create(session=session, role='model', content=ai_text)

            return Response({"response": ai_text}, status=status.HTTP_201_CREATED)

        except errors.ClientError as e:
            if getattr(e, 'code', None) == 429 or '429' in str(e):
                logger.warning(f"Gemini API Quota Exceeded: {str(e)}")
                return Response(
                    {"error": "API 使用量已達上限 (429 Resource Exhausted)，請稍後再試或聯繫管理員更換模型。"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            logger.error(f"GenAI ClientError in ChatView post: {str(e)}", exc_info=True)
            return Response({"error": f"AI 服務連線錯誤: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Error in ChatView post: {str(e)}", exc_info=True)
            return Response({"error": f"AI 處理失敗: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        刪除對話紀錄
        - 若提供 image_url: 刪除該圖片的對話紀錄。
        - 若未提供 image_url: (危險操作) 刪除使用者「所有」對話紀錄。
        """
        image_url = request.data.get('image_url')

        if image_url:
            # 刪除單一圖片的對話
            session = get_object_or_404(ChatSession, user=request.user, image_url=image_url)
            session.messages.all().delete()
            return Response({"message": "對話紀錄已成功清空"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # 刪除所有圖片的對話
            ChatSession.objects.filter(user=request.user).delete()
            return Response({"message": "所有對話紀錄已全部刪除"}, status=status.HTTP_204_NO_CONTENT)