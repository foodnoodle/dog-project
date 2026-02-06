<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 定義變數
const dogImage = ref(''); // 存放狗狗圖片網址

// 定義函式：去 Dog CEO API 抓圖片
const fetchNewDog = async () => {
  try {
    const response = await axios.get('https://dog.ceo/api/breeds/image/random');
    dogImage.value = response.data.message; // API 回傳的格式是 { message: "圖片網址", status: "success" }
  } catch (error) {
    console.error('發生錯誤:', error);
  }
};

// 組件載入時，先抓一張圖
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
      <button class="btn-save">收藏這張</button> 
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
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.image-container {
  margin: 20px 0;
  min-height: 300px; /* 固定高度避免跳動 */
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
  background-color: #ff9800;
  color: white;
}
</style>