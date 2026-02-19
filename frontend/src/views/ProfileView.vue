<template>
    <div class="profile-container">
        <div class="profile-card">
            <h2>👤 個人資料</h2>

            <div v-if="authStore.user" class="user-info">
                <p><strong>使用者名稱：</strong> {{ authStore.user.username }}</p>
                <!-- 可以根據需求顯示更多資訊，例如 Email -->
            </div>

            <div class="actions">
                <h3>危險區域</h3>
                <p class="warning-text">刪除帳號後，您的所有收藏資料將無法復原。</p>
                <button @click="handleDeleteAccount" class="delete-btn">
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
.profile-container {
    display: flex;
    justify-content: center;
    padding: 2rem;
}

.profile-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    text-align: left;
}

h2 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 2rem;
}

.user-info {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}

.actions {
    margin-top: 2rem;
}

h3 {
    color: #e74c3c;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.warning-text {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.delete-btn {
    width: 100%;
    padding: 0.8rem;
    background-color: #fff;
    border: 2px solid #e74c3c;
    color: #e74c3c;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}

.delete-btn:hover {
    background-color: #e74c3c;
    color: white;
}
</style>
