<template>
  <div class="min-h-[80vh] flex justify-center items-center p-4">
    <div
      class="bg-white dark:bg-slate-800 p-8 sm:p-10 rounded-3xl shadow-xl w-full max-w-md text-center border border-slate-100 dark:border-slate-700 transition-all">
      <h2 class="text-2xl font-display font-bold text-slate-800 dark:text-white mb-8">🐶 會員登入</h2>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="text-left">
          <label for="username" class="block mb-2 text-sm font-semibold text-slate-700 dark:text-slate-300">帳號
            (Username)</label>
          <input id="username" v-model="username" type="text" required placeholder="請輸入您的帳號" :disabled="isLoading"
            class="w-full px-4 py-3 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-800 dark:text-white bg-slate-50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed placeholder-slate-400">
        </div>

        <div class="text-left">
          <label for="password" class="block mb-2 text-sm font-semibold text-slate-700 dark:text-slate-300">密碼
            (Password)</label>
          <input id="password" v-model="password" type="password" required placeholder="請輸入您的密碼" :disabled="isLoading"
            class="w-full px-4 py-3 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-800 dark:text-white bg-slate-50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed placeholder-slate-400">
        </div>

        <div v-if="errorMessage"
          class="p-3 text-sm text-red-600 bg-red-50 dark:bg-red-900/30 dark:text-red-400 rounded-lg text-left">
          ⚠️ {{ errorMessage }}
        </div>

        <button type="submit" :disabled="isLoading"
          class="w-full py-3.5 px-4 bg-primary-600 text-white font-bold rounded-xl shadow-lg shadow-primary-500/30 hover:bg-primary-700 hover:-translate-y-0.5 transition-all disabled:opacity-70 disabled:cursor-wait disabled:hover:translate-y-0 disabled:shadow-none">
          <span v-if="isLoading">登入中...</span>
          <span v-else>立即登入</span>
        </button>
      </form>

      <div
        class="mt-8 pt-6 border-t border-slate-100 dark:border-slate-700 text-sm text-slate-500 dark:text-slate-400 space-y-2">
        <p>還沒有帳號？ <router-link to="/register"
            class="text-primary-600 dark:text-primary-400 font-bold hover:underline">立即註冊</router-link></p>
        <div class="mt-4 p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg text-xs">
          <p>測試帳號：TestUser2024</p>
          <p>密碼：MyDogProject01</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth'; // 引入我們寫好的 Store

const router = useRouter();
const authStore = useAuthStore();

// 定義響應式變數
const username = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

// 處理登入邏輯
const handleLogin = async () => {
  // 1. 重置狀態
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // 2. 呼叫 Pinia Store 的登入動作
    await authStore.login(username.value, password.value);

    // 3. 登入成功，跳轉回首頁
    // (小技巧：如果未來有「從哪裡來就回哪裡去」的需求，可以在這裡改)
    router.push('/');

  } catch (error) {
    // 4. 處理錯誤 (如果是 400/401 通常是帳號密碼錯)
    console.error(error);
    if (error.response && (error.response.status === 400 || error.response.status === 401)) {
      errorMessage.value = '帳號或密碼錯誤，請再試一次。';
    } else {
      errorMessage.value = '登入發生異常，請檢查網路連線。';
    }
  } finally {
    // 5. 解除讀取狀態
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* All scoped CSS replaced with Tailwind utility classes in the template */
</style>