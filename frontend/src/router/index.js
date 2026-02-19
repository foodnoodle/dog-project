import { createRouter, createWebHistory } from 'vue-router'
// 引入我們剛才做好的兩個頁面
import HomeView from '../views/HomeView.vue'
import FavoritesView from '../views/FavoritesView.vue'
import LoginView from '../views/LoginView.vue' // 引入登入頁面
import { useAuthStore } from '../stores/auth' // 引入 Pinia Auth Store (為了檢查 Token)
import RegisterView from '../views/RegisterView.vue'; // 引入註冊頁

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
      path: '/login',  // 當網址是 /login 時 (定義登入路徑)
      name: 'login',
      component: LoginView // 顯示登入頁面
    },

    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },

    {
      path: '/favorites', // 當網址是 /favorites 時
      name: 'favorites',
      component: FavoritesView, // 顯示收藏頁
      meta: {
        requiresAuth: true // 加上「需要權限」的標籤 (meta field)
      }
    },

    {
      path: '/profile', // 個人資料頁
      name: 'profile',
      component: () => import('../views/ProfileView.vue'), // Lazy load
      meta: {
        requiresAuth: true
      }
    }

  ]
})

// 💂 設定全域導航守衛 (Global Navigation Guard)
// 每次切換頁面之前，都會執行這個函式
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 檢查目標頁面是否需要權限 (to.meta.requiresAuth)
  // 並且檢查使用者是否尚未登入 (!authStore.isAuthenticated)
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 如果條件符合，強制轉導到登入頁
    next({ name: 'login' })
  } else {
    // 否則，直接放行
    next()
  }
})

export default router