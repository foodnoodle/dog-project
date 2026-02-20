<template>
    <div class="min-h-[80vh] flex justify-center items-start pt-10 px-4">
        <div
            class="bg-white dark:bg-slate-800 p-8 rounded-3xl shadow-xl w-full max-w-md text-left border border-slate-100 dark:border-slate-700 transition-all">
            <h2 class="text-2xl font-display font-bold text-center text-slate-800 dark:text-white mb-8">
                👤 個人資料
            </h2>

            <div v-if="authStore.user"
                class="mb-8 pb-6 border-b border-slate-100 dark:border-slate-700 flex flex-col gap-2">
                <span
                    class="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">使用者帳號</span>
                <p class="text-xl font-medium text-slate-800 dark:text-white">{{ authStore.user.username }}</p>
            </div>

            <div class="mt-8 bg-red-50 dark:bg-red-900/10 p-6 rounded-2xl border border-red-100 dark:border-red-900/30">
                <h3 class="text-red-600 dark:text-red-400 font-bold text-lg mb-2">危險區域</h3>
                <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">
                    刪除帳號後，您的所有收藏資料將無法復原。
                </p>
                <button @click="handleDeleteAccount"
                    class="w-full py-3 px-4 bg-white dark:bg-slate-800 border-2 border-red-500 text-red-500 hover:bg-red-500 hover:text-white font-bold rounded-xl transition-colors duration-300">
                    ⚠️ 刪除我的帳號
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleDeleteAccount = async () => {
    // 1.再一次確認 (防呆)
    const confirmed = confirm('您確定要永久刪除帳號嗎？此動作無法復原！');

    if (!confirmed) return;

    try {
        // 2. 呼叫 Store 的刪除動作
        await authStore.deleteAccount();

        // 3. 成功後跳轉回首頁或登入頁
        alert('帳號已刪除，後會有期！');
        router.push('/login');
    } catch (error) {
        alert('刪除失敗，請稍後再試。');
    }
};
</script>

<style scoped>
/* All scoped CSS replaced with Tailwind utility classes in the template */
</style>
