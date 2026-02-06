<script setup>
import RandomDog from './components/RandomDog.vue';
</script>

<template>
  <div class="app-container">
    <h1>我的狗狗收藏館 🐕</h1>
    <RandomDog />
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

h1 {
  text-align: center;
  color: #333;
}
</style>