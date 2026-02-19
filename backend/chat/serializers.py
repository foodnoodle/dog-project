from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    """
    用於處理單條對話訊息的序列化。
    """
    class Model:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    """
    用於處理對話階段的序列化，並巢狀包含該階段的所有訊息。
    """
    # 使用剛才定義的訊息序列化器，列出該 Session 下的所有對話
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'image_url', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at', 'messages']