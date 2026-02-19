<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api'; // 引入我們封裝好的 api 工具，不再使用 axios
import { useAuthStore } from '../stores/auth';
import { useChatStore } from '../stores/chatStore';

const dogs = ref([]); // 存放從後端抓回來的圖片列表
const authStore = useAuthStore();
const chatStore = useChatStore();

// Modal 狀態與當前要刪除的狗狗 ID
const showDeleteModal = ref(false);
const dogToDelete = ref(null);

// 0. 打開 AI 對話
const openChat = (url) => {
  if (url) {
    chatStore.openDrawer(url);
  }
};

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

// 2. 準備刪除 (點擊刪除按鈕時觸發)
const promptDelete = (id) => {
  dogToDelete.value = id;
  showDeleteModal.value = true;
};

// 3. 確認刪除 (在 Modal 中點擊確認)
const confirmDelete = async () => {
  if (!dogToDelete.value) return;

  try {
    // 呼叫後端 API 刪除該 ID 的資料
    await api.delete(`/api/dogs/${dogToDelete.value}/`);

    // 成功後，重新抓取一次列表，更新畫面
    await fetchFavorites();

    // 關閉 Modal 並清空 ID
    showDeleteModal.value = false;
    dogToDelete.value = null;
  } catch (error) {
    // 如果是伺服器掛了，api.js 會跳全域警告
    // 這裡我們只要保留針對「刪除動作」失敗的提示即可
    alert('刪除失敗');
    console.error(error);
  }
};

// 4. 取消刪除
const cancelDelete = () => {
  showDeleteModal.value = false;
  dogToDelete.value = null;
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
        <div class="actions">
          <button @click="openChat(dog.url)" class="btn-chat" v-if="authStore.isAuthenticated">✨ 詢問 AI</button>
          <button @click="promptDelete(dog.id)" class="btn-delete">刪除</button>
        </div>
      </div>
    </div>

    <!-- 自定義刪除確認 Modal -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal-content">
        <h3>確定要刪除這張狗狗嗎？</h3>
        <p>刪除後將無法復原。</p>
        <div class="modal-actions">
          <button @click="cancelDelete" class="btn-cancel">取消</button>
          <button @click="confirmDelete" class="btn-confirm-delete">確定刪除</button>
        </div>
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
  @apply dark:bg-gray-800 dark:text-white;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
  @apply dark:border-gray-700;
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
  @apply dark:border-gray-700 dark:bg-gray-800;
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

.actions {
  display: flex;
  flex-direction: column;
}

.btn-delete,
.btn-chat {
  width: 100%;
  padding: 8px;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.btn-delete {
  background-color: #ff5252;
}

.btn-chat {
  background-color: #2196F3;
}

.btn-delete:hover,
.btn-chat:hover {
  opacity: 0.9;
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

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  @apply dark:bg-gray-800 dark:text-white;
}

.modal-content h3 {
  margin-top: 0;
  color: #333;
  @apply dark:text-white;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.btn-cancel,
.btn-confirm-delete {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.btn-cancel {
  background-color: #e0e0e0;
  color: #333;
  @apply dark:bg-gray-600 dark:text-white;
}

.btn-confirm-delete {
  background-color: #ff5252;
  color: white;
}

.btn-cancel:hover {
  background-color: #d5d5d5;
}

.btn-confirm-delete:hover {
  background-color: #ff1744;
}
</style>