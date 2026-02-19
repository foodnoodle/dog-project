<script setup>
import { ref, onMounted } from 'vue';
import { chatApi } from '../api/chat';
import { useChatStore } from '../stores/chatStore';

const sessions = ref([]);
const loading = ref(false);
const chatStore = useChatStore();

// 1. 獲取所有對話紀錄
const fetchSessions = async () => {
    loading.value = true;
    try {
        const response = await chatApi.getAllSessions();
        sessions.value = response.data;
    } catch (error) {
        console.error('無法取得對話紀錄:', error);
    } finally {
        loading.value = false;
    }
};

// 2. 打開對話
const openChat = (url) => {
    chatStore.openDrawer(url);
};

// 3. 刪除所有紀錄
const deleteAll = async () => {
    if (!confirm('⚠️ 警告：是否要刪除所有對話紀錄？此動作無法復原！')) return;

    try {
        await chatApi.deleteAllSessions();
        alert('所有對話紀錄已清空');
        fetchSessions(); // 重新整理列表
    } catch (error) {
        alert('刪除失敗');
        console.error(error);
    }
};

onMounted(() => {
    fetchSessions();
});
</script>

<template>
    <div class="history-container">
        <div class="header">
            <h2>📜 歷史對話紀錄</h2>
            <div class="header-actions">
                <button @click="fetchSessions" class="btn-refresh">🔄 刷新</button>
                <button @click="deleteAll" class="btn-delete-all" v-if="sessions.length > 0">🗑️ 刪除全部</button>
            </div>
        </div>

        <div v-if="loading" class="loading">載入中...</div>

        <div v-else-if="sessions.length === 0" class="empty-state">
            目前沒有任何對話紀錄。
        </div>

        <div v-else class="grid">
            <div v-for="session in sessions" :key="session.id" class="grid-item">
                <div class="image-wrapper" @click="openChat(session.image_url)">
                    <img :src="session.image_url" alt="Chat History" loading="lazy" />
                    <div class="overlay">
                        <span>💬 繼續對話</span>
                    </div>
                </div>
                <!-- 格式化時間：雖然 Serializer 有給，但簡單切字串只取日期部分即可 -->
                <div class="meta">
                    <small>{{ new Date(session.created_at).toLocaleString() }}</small>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.history-container {
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

.header-actions {
    display: flex;
    gap: 10px;
}

.btn-refresh,
.btn-delete-all {
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    color: white;
}

.btn-refresh {
    background-color: #2196F3;
}

.btn-refresh:hover {
    background-color: #1976D2;
}

.btn-delete-all {
    background-color: #ff5252;
}

.btn-delete-all:hover {
    background-color: #d32f2f;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
}

.grid-item {
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

.image-wrapper {
    position: relative;
    cursor: pointer;
    height: 150px;
}

.image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* 懸浮時顯示遮罩 */
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
    opacity: 0;
    transition: opacity 0.3s;
}

.image-wrapper:hover .overlay {
    opacity: 1;
}

.meta {
    padding: 8px;
    text-align: center;
    background: #f9f9f9;
    border-top: 1px solid #eee;
    @apply dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300;
}

.empty-state,
.loading {
    text-align: center;
    padding: 40px;
    color: #888;
}
</style>
