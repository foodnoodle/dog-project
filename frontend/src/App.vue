<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header>
      <h1>我的狗狗收藏館 🐕</h1>
      
      <nav>
        <RouterLink to="/" class="nav-link">首頁 (抽卡)</RouterLink>
        <RouterLink to="/favorites" class="nav-link">我的收藏</RouterLink>
      </nav>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
/* 全域設定 */
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f0f2f5;
}

.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

h1 {
  color: #333;
  margin: 0 0 20px 0;
}

nav {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.nav-link {
  text-decoration: none;
  color: #555;
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s;
  background-color: #f8f9fa;
}

/* 當連結被選中時的樣式 (Vue Router 會自動加上這個 class) */
.router-link-active {
  background-color: #4CAF50;
  color: white;
}

.nav-link:hover:not(.router-link-active) {
  background-color: #e9ecef;
  color: #333;
}
</style>