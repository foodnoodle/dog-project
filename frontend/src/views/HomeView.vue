<script setup>
import RandomDog from '../components/RandomDog.vue';
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[80vh]">
    <div class="text-center mb-10 space-y-4 max-w-2xl mx-auto px-4">
      <h1
        class="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-indigo-600 dark:from-primary-400 dark:to-indigo-400 py-2">
        🐶 尋找您的命定狗狗
      </h1>
      <p class="text-lg text-slate-600 dark:text-slate-300">
        點擊按鈕，遇見下一隻可愛夥伴！一起探索狗狗的世界吧。
      </p>
    </div>
    <RandomDog />
  </div>
</template>

<style scoped>
/* Scoped styles removed in favor of Tailwind utility classes */
</style>