<template>
    <div class="min-h-[80vh] flex justify-center items-center px-4 sm:p-4">
        <div
            class="bg-white dark:bg-slate-800 p-6 sm:p-10 rounded-3xl shadow-xl w-full max-w-md text-center border border-slate-100 dark:border-slate-700 transition-all">
            <h2 class="text-2xl font-display font-bold text-slate-800 dark:text-white mb-8">📝 新會員註冊</h2>

            <form @submit.prevent="handleRegister" class="space-y-6">
                <div class="text-left">
                    <label class="block mb-2 text-sm font-semibold text-slate-700 dark:text-slate-300">帳號
                        (Username)</label>
                    <input v-model="username" type="text" required placeholder="請設定您的帳號"
                        class="w-full px-4 py-3 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-800 dark:text-white bg-slate-50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all placeholder-slate-400">
                </div>

                <div class="text-left">
                    <label class="block mb-2 text-sm font-semibold text-slate-700 dark:text-slate-300">密碼
                        (Password)</label>
                    <input v-model="password" type="password" required placeholder="請設定密碼"
                        class="w-full px-4 py-3 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-800 dark:text-white bg-slate-50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all placeholder-slate-400">
                </div>

                <div class="text-left">
                    <label class="block mb-2 text-sm font-semibold text-slate-700 dark:text-slate-300">確認密碼 (Confirm
                        Password)</label>
                    <input v-model="passwordConfirm" type="password" required placeholder="請再次輸入密碼"
                        class="w-full px-4 py-3 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-800 dark:text-white bg-slate-50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all placeholder-slate-400">
                </div>

                <div v-if="errorMessage"
                    class="p-3 text-sm text-red-600 bg-red-50 dark:bg-red-900/30 dark:text-red-400 rounded-lg text-left">
                    ⚠️ {{ errorMessage }}
                </div>

                <button type="submit" :disabled="isLoading"
                    class="w-full py-3.5 px-4 bg-sky-600 text-white font-bold rounded-xl shadow-lg shadow-sky-500/30 hover:bg-sky-700 hover:-translate-y-0.5 transition-all disabled:opacity-70 disabled:cursor-wait disabled:hover:translate-y-0 disabled:shadow-none">
                    {{ isLoading ? '註冊中...' : '立即註冊' }}
                </button>
            </form>

            <div
                class="mt-8 pt-6 border-t border-slate-100 dark:border-slate-700 text-sm text-slate-500 dark:text-slate-400 space-y-2">
                <p>已經有帳號了嗎？ <router-link to="/login"
                        class="text-sky-600 dark:text-sky-400 font-bold hover:underline">按此登入</router-link></p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const passwordConfirm = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const handleRegister = async () => {
    // 1. 前端先檢查密碼是否一致
    if (password.value !== passwordConfirm.value) {
        errorMessage.value = '兩次輸入的密碼不一致！';
        return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    try {
        // 2. 呼叫 Store 的註冊功能
        await authStore.register(username.value, password.value, passwordConfirm.value);

        // 3. 註冊成功 (且自動登入成功)，跳轉首頁
        alert('註冊成功！歡迎加入！🎉');
        router.push('/');

    } catch (error) {
        console.error('完整錯誤訊息:', error.response?.data); // 在 F12 Console 也印一份

        if (error.response && error.response.data) {
            const data = error.response.data;

            // 優先檢查常見錯誤
            if (data.username) {
                errorMessage.value = `帳號錯誤: ${data.username[0]}`;
            } else if (data.password) {
                errorMessage.value = `密碼錯誤: ${data.password[0]}`;
            } else if (data.email) {
                // 抓到了！如果是 Email 錯誤
                errorMessage.value = `Email 錯誤: ${data.email[0]}`;
            } else if (data.non_field_errors) {
                // 抓到了！如果是整體錯誤 (例如密碼太相似)
                errorMessage.value = `註冊失敗: ${data.non_field_errors[0]}`;
            } else {
                // 如果還是抓不到，直接把整個物件轉成文字顯示出來，不再猜謎
                errorMessage.value = `註冊失敗 (詳細): ${JSON.stringify(data)}`;
            }
        } else {
            errorMessage.value = '連線異常，請稍後再試。';
        }
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
/* All scoped CSS replaced with Tailwind utility classes in the template */
</style>