import { createRouter, createWebHistory } from 'vue-router'
// 引入我們剛才做好的兩個頁面
import HomeView from '../views/HomeView.vue'
import FavoritesView from '../views/FavoritesView.vue'

const router = createRouter({
  // 設定歷史模式，讓網址像正常網站一樣 (例如 /favorites)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',          // 當網址是根目錄時
      name: 'home',
      component: HomeView // 顯示首頁
    },
    {
      path: '/favorites', // 當網址是 /favorites 時
      name: 'favorites',
      component: FavoritesView // 顯示收藏頁
    }
  ]
})

export default router