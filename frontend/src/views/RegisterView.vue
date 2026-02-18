<template>
    <div class="register-container">
        <div class="card">
            <h2>📝 新會員註冊</h2>

            <form @submit.prevent="handleRegister" class="register-form">
                <div class="form-group">
                    <label>帳號 (Username)</label>
                    <input v-model="username" type="text" required placeholder="請設定您的帳號">
                </div>

                <div class="form-group">
                    <label>密碼 (Password)</label>
                    <input v-model="password" type="password" required placeholder="請設定密碼">
                </div>

                <div class="form-group">
                    <label>確認密碼 (Confirm Password)</label>
                    <input v-model="passwordConfirm" type="password" required placeholder="請再次輸入密碼">
                </div>

                <div v-if="errorMessage" class="error-message">
                    ⚠️ {{ errorMessage }}
                </div>

                <button type="submit" :disabled="isLoading" class="submit-btn">
                    {{ isLoading ? '註冊中...' : '立即註冊' }}
                </button>
            </form>

            <div class="tips">
                <p>已經有帳號了嗎？ <router-link to="/login">按此登入</router-link></p>
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
/* 樣式直接沿用 LoginView 的 CSS，保持一致性 */
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
}

.card {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    text-align: center;
}

h2 {
    margin-bottom: 1.5rem;
    color: #2c3e50;
}

.form-group {
    margin-bottom: 1.2rem;
    text-align: left;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #34495e;
}

input {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    box-sizing: border-box;
}

input:focus {
    border-color: #42b883;
    outline: none;
}

.submit-btn {
    width: 100%;
    padding: 0.8rem;
    background-color: #3498db;
    /* 註冊按鈕用藍色區隔 */
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
}

.submit-btn:hover {
    background-color: #2980b9;
}

.submit-btn:disabled {
    background-color: #a9cce3;
    cursor: wait;
}

.error-message {
    color: #e74c3c;
    background-color: #fde8e7;
    padding: 0.8rem;
    border-radius: 6px;
    margin-bottom: 1rem;
}

.tips {
    margin-top: 2rem;
    font-size: 0.85rem;
    color: #7f8c8d;
    border-top: 1px solid #eee;
    padding-top: 1rem;
}

a {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}
</style>