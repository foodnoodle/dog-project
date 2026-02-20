<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api';
import { useAuthStore } from '../stores/auth';
import { useChatStore } from '../stores/chatStore';

const dogs = ref([]);
const authStore = useAuthStore();
const chatStore = useChatStore();

const showDeleteModal = ref(false);
const dogToDelete = ref(null);

const openChat = (url) => {
  if (url) {
    chatStore.openDrawer(url);
  }
};

const fetchFavorites = async () => {
  try {
    const response = await api.get('/api/dogs/');
    dogs.value = response.data;
  } catch (error) {
    console.error('無法取得列表:', error);
  }
};

const promptDelete = (id) => {
  dogToDelete.value = id;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  if (!dogToDelete.value) return;
  try {
    await api.delete(`/api/dogs/${dogToDelete.value}/`);
    await fetchFavorites();
    showDeleteModal.value = false;
    dogToDelete.value = null;
  } catch (error) {
    alert('刪除失敗');
    console.error(error);
  }
};

const cancelDelete = () => {
  showDeleteModal.value = false;
  dogToDelete.value = null;
};

onMounted(() => {
  fetchFavorites();
});
</script>

<template>
  <div
    class="bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 md:p-8 transition-all w-full mt-4">
    <div
      class="flex flex-col sm:flex-row justify-between items-center mb-8 pb-4 border-b border-slate-100 dark:border-slate-700 gap-4">
      <h2 class="text-2xl font-display font-bold text-slate-800 dark:text-white">🏆 我的收藏庫</h2>
      <button @click="fetchFavorites" class="btn-primary">
        🔄 刷新列表
      </button>
    </div>

    <div v-if="dogs.length === 0"
      class="flex flex-col items-center justify-center py-16 text-slate-500 dark:text-slate-400">
      <span class="text-4xl mb-3">📭</span>
      <p class="text-lg">還沒有收藏狗狗喔，快去上面抓幾張！</p>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6">
      <div v-for="dog in dogs" :key="dog.id"
        class="group relative bg-slate-100 dark:bg-slate-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
        <div class="aspect-square w-full">
          <img :src="dog.url" alt="Saved Dog"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" loading="lazy" />
        </div>

        <!-- Hover Overlay -->
        <div
          class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-3 gap-2">
          <button @click="openChat(dog.url)" v-if="authStore.isAuthenticated"
            class="w-full py-2 bg-indigo-500/90 hover:bg-indigo-600 text-white text-sm font-medium rounded-lg backdrop-blur-sm transition-colors">
            ✨ 詢問 AI
          </button>
          <button @click="promptDelete(dog.id)"
            class="w-full py-2 bg-red-500/90 hover:bg-red-600 text-white text-sm font-medium rounded-lg backdrop-blur-sm transition-colors">
            🗑️ 刪除
          </button>
        </div>
      </div>
    </div>

    <!-- 自定義刪除確認 Modal -->
    <div v-if="showDeleteModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 dark:bg-slate-950/60 backdrop-blur-sm transition-opacity">
      <div
        class="bg-white dark:bg-slate-800 p-6 md:p-8 rounded-3xl w-full max-w-sm shadow-2xl transform transition-all border border-slate-100 dark:border-slate-700 text-center">
        <div class="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-3xl">⚠️</span>
        </div>
        <h3 class="text-xl font-bold text-slate-800 dark:text-white mb-2">確定要刪除這張狗狗嗎？</h3>
        <p class="text-slate-500 dark:text-slate-400 mb-8">刪除後將無法復原。</p>
        <div class="flex justify-center gap-3">
          <button @click="cancelDelete"
            class="flex-1 py-2.5 px-4 bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 font-medium rounded-xl transition-colors">
            取消
          </button>
          <button @click="confirmDelete"
            class="flex-1 py-2.5 px-4 bg-red-500 hover:bg-red-600 text-white font-medium rounded-xl shadow-lg shadow-red-500/30 transition-all hover:-translate-y-0.5">
            確定刪除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-primary {
  @apply inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-primary-700 bg-primary-50 dark:bg-primary-900/30 dark:text-primary-400 rounded-xl hover:bg-primary-100 dark:hover:bg-primary-900/50 hover:shadow-md hover:-translate-y-0.5 transition-all outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500;
}
</style>