<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api'; // 引入我們封裝好的 api 工具，不再使用 axios

const dogs = ref([]); // 存放從後端抓回來的圖片列表

// 1. 獲取收藏列表 (GET)
const fetchFavorites = async () => {
  try {
    // api 實體會自動補上 base URL
    const response = await api.get('/api/dogs/');
    dogs.value = response.data;
  } catch (error) {
    console.error('無法取得列表:', error);
  }
};

// 2. 刪除圖片 (DELETE) - 這是加碼功能
const deleteDog = async (id) => {
  if (!confirm('確定要刪除這張狗狗嗎？')) return;

  try {
    // 呼叫後端 API 刪除該 ID 的資料
    await api.delete(`/api/dogs/${id}/`);

    fetchFavorites(); // 成功後，重新抓取一次列表，更新畫面
  } catch (error) {
    // 如果是伺服器掛了，api.js 會跳全域警告
    // 這裡我們只要保留針對「刪除動作」失敗的提示即可
    alert('刪除失敗');
    console.error(error);
  }
};

// 組件載入時執行
onMounted(() => {
  fetchFavorites();
});
</script>

<template>
  <div class="list-container">
    <div class="header">
      <h2>🏆 我的收藏庫</h2>
      <button @click="fetchFavorites" class="btn-refresh">刷新列表</button>
    </div>

    <div v-if="dogs.length === 0" class="empty-state">
      還沒有收藏狗狗喔，快去上面抓幾張！
    </div>

    <div class="grid">
      <div v-for="dog in dogs" :key="dog.id" class="grid-item">
        <img :src="dog.url" alt="Saved Dog" />
        <button @click="deleteDog(dog.id)" class="btn-delete">刪除</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.list-container {
  margin-top: 40px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.grid {
  display: grid;
  /* RWD 設定：自動填滿，每欄最小 150px */
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}

.grid-item {
  position: relative;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.grid-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.grid-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}

.btn-delete {
  width: 100%;
  padding: 8px;
  background-color: #ff5252;
  color: white;
  border: none;
  cursor: pointer;
  opacity: 0.9;
}

.btn-delete:hover {
  opacity: 1;
  background-color: #d32f2f;
}

.btn-refresh {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.empty-state {
  text-align: center;
  color: #888;
  padding: 20px;
}
</style>