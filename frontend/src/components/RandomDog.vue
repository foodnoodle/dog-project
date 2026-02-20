<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api'; // 引入我們封裝好的 api 工具
import axios from 'axios'; // 引入 axios，為了抓取外部 API 的圖片
import { useAuthStore } from '../stores/auth'; // 引入 auth store
import { useChatStore } from '../stores/chatStore'; // 引入 chat store

const dogImage = ref('');
const isImageLoading = ref(true);
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
  isImageLoading.value = true;
  try {
    const response = await axios.get('https://dog.ceo/api/breeds/image/random');
    dogImage.value = response.data.message;
  } catch (error) {
    console.error('抓取圖片失敗:', error);
  } finally {
    isImageLoading.value = false;
  }
};

// 2. 收藏圖片到 Django 後端
const saveDog = async () => {
  if (!dogImage.value) return;

  if (!authStore.isAuthenticated) {
    alert('請先登入才能收藏');
    return;
  }

  try {
    const response = await api.post('/api/dogs/', {
      url: dogImage.value
    });
    alert('收藏成功！');
    console.log('後端回應:', response.data);
  } catch (error) {
    console.error('收藏失敗:', error);
  }
};

onMounted(() => {
  fetchNewDog();
});
</script>

<template>
  <div
    class="w-full max-w-md mx-auto bg-white dark:bg-slate-800 rounded-3xl shadow-xl dark:shadow-slate-900/50 overflow-hidden border border-slate-100 dark:border-slate-700 transition-all hover:shadow-2xl">

    <!-- Image Header -->
    <div class="relative w-full h-80 bg-slate-100 dark:bg-slate-700/50 flex items-center justify-center p-4">
      <div v-if="isImageLoading" class="animate-pulse flex flex-col items-center justify-center space-y-4">
        <div class="w-12 h-12 bg-slate-300 dark:bg-slate-600 rounded-full"></div>
        <div class="h-4 bg-slate-300 dark:bg-slate-600 rounded w-24"></div>
      </div>
      <img v-else-if="dogImage" :src="dogImage" alt="Random Dog"
        class="max-w-full max-h-full object-contain rounded-xl drop-shadow-md" loading="lazy" />
      <div v-else class="text-slate-500 dark:text-slate-400 flex flex-col items-center">
        <span class="text-3xl mb-2">🐕</span>
        <span>無法載入圖片</span>
      </div>

      <!-- Gradient overlay to blend bottom part -->
      <div class="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-white dark:from-slate-800 to-transparent">
      </div>
    </div>

    <!-- Content & Controls -->
    <div class="relative z-10 p-6 -mt-6 bg-white dark:bg-slate-800 rounded-t-3xl">
      <h2 class="text-xl font-display font-bold text-center text-slate-800 dark:text-white mb-6">
        🐶 您的隨機狗狗
      </h2>

      <div class="flex flex-col gap-3">
        <button @click="fetchNewDog" class="btn-primary w-full group">
          <span class="mr-2 group-hover:rotate-180 transition-transform duration-300 inline-block">🎲</span> 換一張
        </button>

        <div class="grid grid-cols-2 gap-3">
          <button @click="saveDog" class="btn-secondary">
            💖 收藏這張
          </button>

          <button @click="openChat" v-if="dogImage && authStore.isAuthenticated" class="btn-ai">
            ✨ 詢問 AI
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-primary {
  @apply relative overflow-hidden inline-flex items-center justify-center px-6 py-3 text-base font-medium text-white bg-primary-600 rounded-xl hover:bg-primary-700 hover:shadow-lg hover:-translate-y-0.5 shadow-primary-500/30 transition-all duration-300 outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-600 dark:focus:ring-offset-slate-900;
}

.btn-secondary {
  @apply inline-flex items-center justify-center px-4 py-3 text-sm font-medium text-pink-600 bg-pink-50 dark:bg-pink-900/30 rounded-xl hover:bg-pink-100 dark:hover:bg-pink-900/50 hover:text-pink-700 dark:text-pink-400 hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 dark:focus:ring-offset-slate-900;
}

.btn-ai {
  @apply inline-flex items-center justify-center px-4 py-3 text-sm font-medium text-indigo-600 bg-indigo-50 dark:bg-indigo-900/30 rounded-xl hover:bg-indigo-100 dark:hover:bg-indigo-900/50 hover:text-indigo-700 dark:text-indigo-400 hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-slate-900;
}
</style>