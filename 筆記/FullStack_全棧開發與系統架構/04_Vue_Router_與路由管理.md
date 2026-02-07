# Vue Router 與路由管理

## 第一章：單頁應用 (SPA) 概念

### 傳統網頁 vs SPA

**傳統網頁（多頁應用）：**
```
用戶點擊連結
  ↓
瀏覽器發送 HTTP 請求
  ↓
伺服器返回完整 HTML 頁面
  ↓
瀏覽器重新載入整個頁面
  ↓
頁面閃爍，用戶體驗差
```

**單頁應用 (SPA)：**
```
用戶點擊連結
  ↓
JavaScript 路由攔截（不傳送 HTTP 請求）
  ↓
動態改變模版內容
  ↓
URL 更新，但頁面不重載
  ↓
無閃爍，用戶體驗流暢
```

### SPA 的優勢

| 優勢 | 說明 |
|------|------|
| 快速導航 | 無需重新載入頁面 |
| 離線能力 | 可以實現離線功能 |
| 原生應用感受 | 更像桌面應用 |
| 降低伺服器負擔 | 減少 HTML 傳輸 |

---

## 第二章：Vue Router 基礎

### 路由的概念

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FavoritesView from '../views/FavoritesView.vue'

const router = createRouter({
  // 歷史模式：URL 看起來像正常網址
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: [
    {
      path: '/',           // 路由路徑
      name: 'home',        // 路由名稱
      component: HomeView  // 要顯示的組件
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FavoritesView
    }
  ]
})

export default router
```

### 路由配置詳解

| 屬性 | 說明 | 例子 |
|------|------|------|
| `path` | URL 路徑 | `/favorites` |
| `name` | 路由唯一名稱 | `'favorites'` |
| `component` | 要顯示的 Vue 組件 | `FavoritesView` |
| `redirect` | 重定向到另一個路由 | `redirect: '/'` |
| `children` | 嵌套路由 | `[{ path: 'detail', component: ... }]` |

---

## 第三章：導航與連結

### RouterLink 組件

```vue
<template>
  <!-- 使用 RouterLink 進行導航 -->
  <nav>
    <!-- to 屬性指定目標路由 -->
    <RouterLink to="/">首頁 (抽卡)</RouterLink>
    <RouterLink to="/favorites">我的收藏</RouterLink>
  </nav>
</template>
```

**RouterLink 的優勢：**
- 自動監聽活躍路由，添加 `.router-link-active` 類名
- 支援路由參數和命名路由
- 在 SPA 中進行無刷新導航

### 活躍連結樣式

```css
/* RouterLink 自動添加的類名 */
.router-link-active {
  color: #ff6b6b;
  font-weight: bold;
}

/* 精確匹配時 */
.router-link-exact-active {
  border-bottom: 2px solid #ff6b6b;
}
```

```vue
<script setup>
import { useRoute } from 'vue-router'

// 手動檢查當前路由
const route = useRoute()
const isActive = route.path === '/'
</script>
```

---

## 第四章：路由視圖與組件顯示

### RouterView 組件

```vue
<!-- App.vue -->
<template>
  <div class="app-container">
    <header>
      <h1>我的狗狗收藏館 🐕</h1>
      <nav>
        <RouterLink to="/">首頁</RouterLink>
        <RouterLink to="/favorites">我的收藏</RouterLink>
      </nav>
    </header>

    <!-- RouterView：根據當前路由顯示對應組件 -->
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
```

**工作流程：**
```
用戶訪問 / → Route 匹配 → HomeView 組件
用戶訪問 /favorites → Route 匹配 → FavoritesView 組件
↓
組件內容被插入到 <RouterView /> 位置
↓
頁面更新，URL 改變，無需重載
```

---

## 第五章：動態路由參數

### 路由參數的定義與使用

```javascript
// 路由配置
const routes = [
  {
    path: '/dog/:id',  // :id 是動態參數佔位符
    name: 'dogDetail',
    component: DogDetailView
  }
]
```

**在組件中訪問參數：**
```vue
<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

// 取得路由參數
const dogId = route.params.id

console.log(dogId)  // 當 URL 是 /dog/5 時，輸出 5
</script>
```

### 編程式導航

```javascript
import { useRouter } from 'vue-router'

const router = useRouter()

// 導航到具體路由
const goToDetail = (id) => {
  router.push(`/dog/${id}`)
  // 或使用命名路由
  router.push({ name: 'dogDetail', params: { id: id } })
}

// 返回上一頁
const goBack = () => {
  router.back()
}

// 替換當前歷史記錄
const replaceRoute = () => {
  router.replace('/home')
}
```

---

## 第六章：查詢參數 (Query Parameters)

### URL 查詢字符串

```javascript
// URL 範例：/favorites?sort=date&filter=saved

import { useRoute } from 'vue-router'

const route = useRoute()

// 訪問查詢參數
const sortBy = route.query.sort      // 'date'
const filterType = route.query.filter // 'saved'
```

**導航時傳遞查詢參數：**
```javascript
const router = useRouter()

// 方法 1：直接在 URL 中
router.push('/favorites?sort=date&filter=saved')

// 方法 2：使用物件（推薦）
router.push({
  path: '/favorites',
  query: { sort: 'date', filter: 'saved' }
})
```

---

## 第七章：嵌套路由

### 路由層級結構

```javascript
const routes = [
  {
    path: '/user/:id',
    component: UserLayout,
    children: [
      {
        path: 'profile',      // 完整路徑：/user/:id/profile
        component: UserProfile
      },
      {
        path: 'settings',     // 完整路徑：/user/:id/settings
        component: UserSettings
      }
    ]
  }
]
```

**父組件使用 RouterView：**
```vue
<!-- UserLayout.vue -->
<template>
  <div class="user-layout">
    <aside>
      <RouterLink to="profile">個人資料</RouterLink>
      <RouterLink to="settings">設定</RouterLink>
    </aside>
    
    <!-- 子路由的組件顯示在這裡 -->
    <main>
      <RouterView />
    </main>
  </div>
</template>
```

---

## 第八章：導航守衛（Route Guards）

### 全域守衛

```javascript
const router = createRouter({ ... })

// 每次導航前執行
router.beforeEach((to, from, next) => {
  console.log(`從 ${from.path} 導航到 ${to.path}`)
  
  // 檢查認證
  if (to.path === '/admin' && !isAuthenticated()) {
    next('/login')  // 重定向到登入頁
  } else {
    next()  // 允許導航
  }
})

// 導航完成後執行
router.afterEach((to, from) => {
  // 更新頁面標題
  document.title = to.meta.title || '應用'
})
```

### 路由級別守衛

```javascript
const routes = [
  {
    path: '/admin',
    component: AdminView,
    beforeEnter: (to, from, next) => {
      // 只有管理員可以進入
      if (hasAdminRole()) {
        next()
      } else {
        next('/forbidden')
      }
    }
  }
]
```

---

## 第九章：路由元資訊與懶加載

### 路由元資訊

```javascript
const routes = [
  {
    path: '/',
    component: HomeView,
    meta: {
      title: '首頁 - 狗狗收藏館',
      requiresAuth: false
    }
  },
  {
    path: '/admin',
    component: AdminView,
    meta: {
      title: '管理後台',
      requiresAuth: true,
      role: 'admin'
    }
  }
]

// 在守衛中使用
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isLoggedIn()) {
    next('/login')
  } else {
    next()
  }
})
```

### 懶加載組件

```javascript
// 方法 1：動態 import（推薦）
const routes = [
  {
    path: '/lazy',
    component: () => import('../views/LazyView.vue')
  }
]

// 方法 2：webpack 魔術註解
const routes = [
  {
    path: '/chunk1',
    component: () => import(
      /* webpackChunkName: "group-a" */
      '../views/Chunk1.vue'
    )
  },
  {
    path: '/chunk2',
    component: () => import(
      /* webpackChunkName: "group-a" */
      '../views/Chunk2.vue'
    )
  }
]
```

**懶加載的優勢：**
- 減少初始包大小
- 按需加載頁面邏輯
- 提升首屏速度

---

## 總結

Vue Router 提供：
✅ 強大的路由系統
✅ 無刷新頁面導航
✅ 動態參數與查詢字符串
✅ 嵌套路由支持
✅ 導航守衛與認證
✅ 懶加載組件優化
