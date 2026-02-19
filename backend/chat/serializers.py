from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    """
    用於處理單條對話訊息的序列化。
    """
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    """
    用於處理對話階段的序列化，並巢狀包含該階段的所有訊息。
    """
    # 使用剛才定義的訊息序列化器，列出該 Session 下的所有對話
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta: # 這是 Django Rest Framework 的固定寫法，用來告訴序列化器要操作哪個模型
        model = ChatSession
        fields = ['id', 'image_url', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at', 'messages']

class ChatSessionListSerializer(serializers.ModelSerializer):
    """
    用於列表顯示的輕量級序列化器，不包含詳細訊息。
    """
    class Meta:
        model = ChatSession
        fields = ['id', 'image_url', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatInputSerializer(serializers.Serializer):
    """專門用於定義發問時的輸入格式"""
    image_url = serializers.URLField(help_text="狗狗圖片的網址")
    prompt = serializers.CharField(help_text="您想問 AI 的提示詞")