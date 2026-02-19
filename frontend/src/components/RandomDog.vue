<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api'; // 引入我們封裝好的 api 工具
import axios from 'axios'; // 引入 axios，為了抓取外部 API 的圖片
import { useAuthStore } from '../stores/auth'; // 引入 auth store
import { useChatStore } from '../stores/chatStore'; // 引入 chat store

const dogImage = ref('');
const authStore = useAuthStore(); // 初始化 auth store
const chatStore = useChatStore(); // 初始化 chat store

// 0. 打開 AI 對話
const openChat = () => {
  if (dogImage.value) {
    chatStore.openDrawer(dogImage.value);
  }
};

// 1. 抓取隨機圖片
const fetchNewDog = async () => {
  try {
    // 這裡雖然是外部網址，但 api 實體一樣可以處理。
    // 使用 axios.get 來抓取外部 API 的圖片
    const response = await axios.get('https://dog.ceo/api/breeds/image/random');
    dogImage.value = response.data.message;
  } catch (error) {
    console.error('抓取圖片失敗:', error);
  }
};

// 2. 收藏圖片到 Django 後端
const saveDog = async () => {
  if (!dogImage.value) return; // 如果沒圖片就不執行

  // 檢查是否登入
  if (!authStore.isAuthenticated) {
    alert('請先登入才能收藏'); // 跳出提示
    return;
  }

  try {
    // 發送 POST 請求給我們的 Django API
    // [重點] 這裡不再寫死 http://127.0.0.1:8000
    // api 實體會自動讀取環境變數 VITE_API_BASE_URL 並拼貼上去
    // 我們只要寫「相對路徑」即可
    const response = await api.post('/api/dogs/', {
      url: dogImage.value
    });

    // 成功提示 (簡單用 alert，之後可以優化)
    alert('收藏成功！');
    console.log('後端回應:', response.data);

  } catch (error) {
    // 錯誤的大部分處理 (如伺服器沒開) 已經在 api.js 的攔截器做完了
    // 這裡只要處理「收藏特定失敗」的邏輯即可
    console.error('收藏失敗:', error);
  }
};

onMounted(() => {
  fetchNewDog();
});
</script>

<template>
  <div class="dog-card">
    <h2>🐶 隨機狗狗</h2>

    <div class="image-container">
      <img v-if="dogImage" :src="dogImage" alt="Random Dog" />
      <p v-else>載入中...</p>
    </div>

    <div class="button-group">
      <button @click="fetchNewDog" class="btn-refresh">換一張</button>
      <button @click="saveDog" class="btn-save">收藏這張</button>
      <button @click="openChat" class="btn-chat" v-if="dogImage">✨ 詢問 AI</button>
    </div>
  </div>
</template>

<style scoped>
/* 手寫 CSS 練習區 */
.dog-card {
  border: 2px solid #ddd;
  padding: 20px;
  border-radius: 12px;
  max-width: 400px;
  margin: 20px auto;
  text-align: center;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.image-container {
  margin: 20px 0;
  min-height: 300px;
  /* 固定高度避免跳動 */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: opacity 0.2s;
}

button:hover {
  opacity: 0.8;
}

.btn-refresh {
  background-color: #4CAF50;
  color: white;
}

.btn-save {
  background-color: #9c27b0;
  color: white;
}

.btn-chat {
  background-color: #2196F3;
  color: white;
}
</style>