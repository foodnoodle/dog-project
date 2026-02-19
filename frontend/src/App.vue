<template>
  <div class="app-container">
    <nav class="navbar">
      <div class="nav-brand">🐶 狗狗圖鑑</div>
      <div class="nav-links">
        <router-link to="/" class="nav-item">首頁 (抽卡)</router-link>

        <template v-if="authStore.isAuthenticated">
          <router-link to="/profile" class="nav-item">個人資料</router-link>
          <router-link to="/favorites" class="nav-item">我的收藏</router-link>
          <router-link to="/history" class="nav-item">對話紀錄</router-link>
          <button @click="handleLogout" class="nav-item logout-btn">登出</button>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-item login-btn">登入</router-link>
          <router-link to="/register" class="nav-item register-btn">註冊</router-link>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <Teleport to="body">
      <ChatDrawer />
    </Teleport>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import ChatDrawer from './components/ChatDrawer.vue';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  // 1. 清除狀態與 Token
  authStore.logout();

  // 2. 強制跳轉回首頁 (或是登入頁)
  router.push('/login');

  // 3. (選用) 跳個通知
  alert('您已成功登出');
};
</script>

<style scoped>
.app-container {
  font-family: Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}

.navbar {
  background-color: #42b883;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-brand {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
  cursor: pointer;
  background: none;
  border: none;
  font-size: 1rem;
  padding: 0;
}

.nav-item:hover {
  opacity: 0.8;
}

/* 特別樣式：登入/註冊/登出按鈕 */
.login-btn,
.register-btn,
.logout-btn {
  background-color: white;
  color: #42b883;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
}

.logout-btn {
  background-color: #e74c3c;
  /* 紅色 */
  color: white;
}

.main-content {
  padding: 2rem;
}
</style>