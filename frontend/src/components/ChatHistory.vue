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
    <div
        class="bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 md:p-8 w-full mt-4">
        <div
            class="flex flex-col sm:flex-row justify-between items-center mb-8 pb-4 border-b border-slate-100 dark:border-slate-700 gap-4">
            <h2 class="text-2xl font-display font-bold text-slate-800 dark:text-white">📜 歷史對話紀錄</h2>
            <div class="flex gap-2">
                <button @click="fetchSessions" class="btn-primary">🔄 刷新</button>
                <button @click="deleteAll" v-if="sessions.length > 0" class="btn-danger">🗑️ 刪除全部</button>
            </div>
        </div>

        <div v-if="loading" class="flex justify-center p-12">
            <span class="text-slate-500 animate-pulse">載入中...</span>
        </div>

        <div v-else-if="sessions.length === 0"
            class="flex flex-col items-center justify-center py-16 text-slate-500 dark:text-slate-400">
            <span class="text-4xl mb-3">📭</span>
            <p class="text-lg">目前沒有任何對話紀錄。</p>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6">
            <div v-for="session in sessions" :key="session.id"
                class="group relative bg-slate-100 dark:bg-slate-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer flex flex-col"
                @click="openChat(session.image_url)">
                <div class="relative w-full aspect-square overflow-hidden">
                    <img :src="session.image_url" alt="Chat History"
                        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                        loading="lazy" />
                    <!-- Hover Overlay -->
                    <div
                        class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex justify-center items-center">
                        <span
                            class="px-4 py-2 bg-white/20 backdrop-blur-md rounded-xl text-white font-medium text-sm">💬
                            繼續對話</span>
                    </div>
                </div>

                <div
                    class="p-3 text-center bg-slate-50 dark:bg-slate-800 border-t border-slate-100 dark:border-slate-700">
                    <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">
                        {{ new Date(session.created_at).toLocaleString() }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.btn-primary {
    @apply inline-flex items-center justify-center px-4 py-2 mt-4 sm:mt-0 text-sm font-medium text-sky-700 bg-sky-50 dark:bg-sky-900/30 dark:text-sky-400 rounded-xl hover:bg-sky-100 dark:hover:bg-sky-900/50 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 outline-none;
}

.btn-danger {
    @apply inline-flex items-center justify-center px-4 py-2 mt-4 sm:mt-0 text-sm font-medium text-red-700 bg-red-50 dark:bg-red-900/30 dark:text-red-400 rounded-xl hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-red-500 outline-none;
}
</style>
