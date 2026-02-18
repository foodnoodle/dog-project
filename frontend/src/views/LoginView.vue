<template>
  <div class="login-container">
    <div class="card">
      <h2>🐶 會員登入</h2>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">帳號 (Username)</label>
          <input id="username" v-model="username" type="text" required placeholder="請輸入您的帳號" :disabled="isLoading">
        </div>

        <div class="form-group">
          <label for="password">密碼 (Password)</label>
          <input id="password" v-model="password" type="password" required placeholder="請輸入您的密碼" :disabled="isLoading">
        </div>

        <div v-if="errorMessage" class="error-message">
          ⚠️ {{ errorMessage }}
        </div>

        <button type="submit" :disabled="isLoading" class="submit-btn">
          <span v-if="isLoading">登入中...</span>
          <span v-else>立即登入</span>
        </button>
      </form>

      <div class="tips">
        <p>還沒有帳號？ <router-link to="/register">立即註冊</router-link></p>
        <p class="test-account">測試帳號：TestUser2024 / 密碼：TestUser2024</p>
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  /* 讓它盡量置中 */
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
  transition: border-color 0.3s;
  box-sizing: border-box;
  /* 確保 padding 不會撐爆寬度 */
}

input:focus {
  border-color: #42b883;
  outline: none;
}

input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.submit-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  background-color: #3aa876;
}

.submit-btn:disabled {
  background-color: #a8d5c2;
  cursor: wait;
}

.error-message {
  color: #e74c3c;
  background-color: #fde8e7;
  padding: 0.8rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.tips {
  margin-top: 2rem;
  font-size: 0.85rem;
  color: #7f8c8d;
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

a {
  color: #42b883;
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}

.test-account {
  font-size: 0.8rem;
  color: #bdc3c7;
  margin-top: 0.5rem;
}
</style>