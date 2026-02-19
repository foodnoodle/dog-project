from django.urls import path
from .views import ChatView

urlpatterns = [
    # 這將對應到 /api/chat/ask/
    path('ask/', ChatView.as_view(), name='chat-ask'),
]