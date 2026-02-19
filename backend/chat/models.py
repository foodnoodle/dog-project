from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    """
    定義一個對話階段，將使用者與特定的狗狗圖片網址綁定。
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 確保同一個使用者對同一張圖片只會產生一個對話 Session
        unique_together = ('user', 'image_url')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.image_url[:30]}..."

class ChatMessage(models.Model):
    """
    儲存對話階段中的每一條具體訊息。
    """
    ROLE_CHOICES = (
        ('user', 'User'),
        ('model', 'Model'),
    )
    
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # 對話依時間正序排列，方便前端直接渲染

    def __str__(self):
        return f"{self.role}: {self.content[:20]}..."