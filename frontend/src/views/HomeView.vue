<script setup>
import RandomDog from '../components/RandomDog.vue';
</script>

<template>
  <div class="home-page">
    <div class="hero-section">
      <h2>🐶 尋找您的命定狗狗</h2>
      <p>點擊按鈕，遇見下一隻可愛夥伴！</p>
    </div>
    <RandomDog />
  </div>
</template>

<style scoped>
.hero-section {
  text-align: center;
  margin-bottom: 20px;
  color: #555;
}
</style>