import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      usePolling: true, // 關鍵：在 Docker 容器內強制使用輪詢模式監控變更
    },
  },
})