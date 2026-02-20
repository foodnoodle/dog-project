<template>
  <div
    class="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans transition-colors duration-300 flex flex-col overflow-x-hidden">
    <!-- Navbar -->
    <nav
      class="sticky top-0 z-40 w-full backdrop-blur-md bg-white/70 dark:bg-slate-900/80 border-b border-slate-200 dark:border-slate-800 transition-all">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Brand -->
          <div class="flex-shrink-0 flex items-center gap-2">
            <span class="text-2xl">🐶</span>
            <span class="font-display font-bold text-xl tracking-tight text-slate-800 dark:text-white">狗狗圖鑑</span>
          </div>

          <!-- Mobile menu button -->
          <div class="flex items-center md:hidden">
            <button @click="isMobileMenuOpen = !isMobileMenuOpen"
              class="w-10 h-10 flex flex-col justify-center items-center rounded-md text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none">
              <span class="block w-5 h-0.5 bg-current transition-all duration-300"
                :class="{ 'rotate-45 translate-y-1.5': isMobileMenuOpen, '-translate-y-1': !isMobileMenuOpen }"></span>
              <span class="block w-5 h-0.5 bg-current transition-all duration-300 my-1"
                :class="{ 'opacity-0': isMobileMenuOpen }"></span>
              <span class="block w-5 h-0.5 bg-current transition-all duration-300"
                :class="{ '-rotate-45 -translate-y-1.5': isMobileMenuOpen, 'translate-y-1': !isMobileMenuOpen }"></span>
            </button>
          </div>

          <!-- Desktop Navigation Links -->
          <div class="hidden md:flex items-center gap-2 md:gap-4">
            <router-link to="/" class="nav-link">首頁 (抽卡)</router-link>

            <template v-if="authStore.isAuthenticated">
              <router-link to="/profile" class="nav-link">個人資料</router-link>
              <router-link to="/favorites" class="nav-link">我的收藏</router-link>
              <router-link to="/history" class="nav-link">對話紀錄</router-link>
              <button @click="handleLogout" class="btn-danger ml-2">登出</button>
            </template>

            <template v-else>
              <router-link to="/login" class="nav-link">登入</router-link>
              <router-link to="/register" class="btn-primary ml-2">註冊</router-link>
            </template>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation Menu Dropdown -->
      <div v-show="isMobileMenuOpen"
        class="md:hidden bg-white/95 dark:bg-slate-900/95 border-b border-slate-200 dark:border-slate-800 px-4 pt-2 pb-4 space-y-2 shadow-lg absolute w-full left-0 z-50 transition-all duration-300">
        <router-link to="/" class="nav-link block w-full text-center" @click="isMobileMenuOpen = false">首頁
          (抽卡)</router-link>

        <template v-if="authStore.isAuthenticated">
          <router-link to="/profile" class="nav-link block w-full text-center"
            @click="isMobileMenuOpen = false">個人資料</router-link>
          <router-link to="/favorites" class="nav-link block w-full text-center"
            @click="isMobileMenuOpen = false">我的收藏</router-link>
          <router-link to="/history" class="nav-link block w-full text-center"
            @click="isMobileMenuOpen = false">對話紀錄</router-link>
          <button @click="handleLogout" class="btn-danger block w-full mt-4">登出</button>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link block w-full text-center"
            @click="isMobileMenuOpen = false">登入</router-link>
          <router-link to="/register" class="btn-primary block w-full text-center mt-4"
            @click="isMobileMenuOpen = false">註冊</router-link>
        </template>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
      <router-view></router-view>
    </main>

    <Teleport to="body">
      <ChatDrawer />
      <ThemeToggle />
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import ChatDrawer from './components/ChatDrawer.vue';
import ThemeToggle from './components/ThemeToggle.vue';

const isMobileMenuOpen = ref(false);

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
.nav-link {
  @apply text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors rounded-md px-3 py-2;
}

.nav-link.router-link-active {
  @apply text-primary-700 dark:text-primary-400 bg-primary-50 dark:bg-slate-800/50;
}

.btn-primary {
  @apply inline-flex items-center justify-center px-5 py-2.5 text-sm font-medium text-white bg-primary-600 rounded-full hover:bg-primary-700 hover:shadow-lg hover:-translate-y-0.5 shadow-primary-500/30 transition-all duration-200 outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-600 dark:focus:ring-offset-slate-900;
}

.btn-danger {
  @apply inline-flex items-center justify-center px-5 py-2.5 text-sm font-medium text-white bg-red-500 rounded-full hover:bg-red-600 hover:shadow-lg hover:-translate-y-0.5 shadow-red-500/30 transition-all duration-200 outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 dark:focus:ring-offset-slate-900;
}
</style>