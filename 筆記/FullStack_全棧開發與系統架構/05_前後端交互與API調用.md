# 前後端交互與 API 調用

## 第一章：HTTP 請求與 Axios

### HTTP 協議基礎

HTTP (HyperText Transfer Protocol) 是網際網路通信的基礎協議。

**請求-回應模式：**
```
客戶端（前端） → HTTP 請求 → 伺服器（後端）
客戶端（前端） ← HTTP 回應 ← 伺服器（後端）
```

### Axios 介紹

Axios 是基於 Promise 的 HTTP 客戶端，用於前端與後端通信。

**相比原生 fetch 的優勢：**
| 特性 | Axios | Fetch |
|------|-------|-------|
| 請求攔截 | ✅ | ❌ |
| 超時設定 | ✅ | 需自己實現 |
| 請求轉換 | ✅ 自動 | ❌ 手動 |
| 使用簡易度 | ✅ 簡潔 | ❌ 冗長 |

---

## 第二章：Axios 基本使用

### 安裝與配置

```bash
npm install axios
```

```javascript
// main.js 中配置 Axios
import axios from 'axios'

// 設定基礎 URL
axios.defaults.baseURL = 'http://127.0.0.1:8000/api'

// 設定超時時間
axios.defaults.timeout = 5000
```

### 基本 CRUD 操作

```javascript
import axios from 'axios'

// GET：取得資料
const fetchDogs = async () => {
  try {
    const response = await axios.get('/dogs/')
    console.log(response.data)  // 回應資料
  } catch (error) {
    console.error('取得失敗:', error)
  }
}

// POST：建立資料
const saveDog = async (dogUrl) => {
  try {
    const response = await axios.post('/dogs/', {
      url: dogUrl
    })
    console.log('保存成功:', response.data.id)
  } catch (error) {
    console.error('保存失敗:', error)
  }
}

// PUT：完全更新
const updateDog = async (id, dogUrl) => {
  await axios.put(`/dogs/${id}/`, {
    url: dogUrl
  })
}

// PATCH：部分更新
const partialUpdate = async (id, dogUrl) => {
  await axios.patch(`/dogs/${id}/`, {
    url: dogUrl
  })
}

// DELETE：刪除資料
const deleteDog = async (id) => {
  await axios.delete(`/dogs/${id}/`)
}
```

---

## 第三章：非同步操作與 async/await

### Promise 與 async/await

**傳統 Promise 寫法：**
```javascript
axios.get('/dogs/')
  .then(response => {
    console.log(response.data)
  })
  .catch(error => {
    console.error('錯誤:', error)
  })
```

**async/await 寫法（推薦）：**
```javascript
const fetchDogs = async () => {
  try {
    const response = await axios.get('/dogs/')
    console.log(response.data)
  } catch (error) {
    console.error('錯誤:', error)
  }
}
```

### async/await 的優勢

1. **可讀性更高**：看起來像同步代碼
2. **錯誤處理簡潔**：使用 try-catch
3. **避免回調地獄**：代碼結構清晰

### 例子：順序執行多個請求

```javascript
const processMultipleRequests = async () => {
  try {
    // 先取得所有狗狗
    const dogsResponse = await axios.get('/dogs/')
    const dogs = dogsResponse.data
    
    // 然後處理每一隻狗狗
    for (const dog of dogs) {
      await axios.post('/process-dog/', { id: dog.id })
    }
    
    console.log('全部完成')
  } catch (error) {
    console.error('流程失敗:', error)
  }
}
```

### 並行執行多個請求

```javascript
import axios from 'axios'

const fetchAllData = async () => {
  try {
    // 同時發送多個請求，等所有完成
    const [dogsRes, usersRes, statsRes] = await Promise.all([
      axios.get('/dogs/'),
      axios.get('/users/'),
      axios.get('/stats/')
    ])
    
    console.log('狗狗數:', dogsRes.data.length)
    console.log('使用者數:', usersRes.data.length)
    console.log('統計:', statsRes.data)
  } catch (error) {
    console.error('至少一個請求失敗:', error)
  }
}
```

---

## 第四章：回應資料結構

### 典型的 API 回應

```javascript
const response = await axios.get('/dogs/')

// response 物件結構
{
  data: [            // 實際資料
    { id: 1, url: '...', created_at: '2024-01-01' },
    { id: 2, url: '...', created_at: '2024-01-02' }
  ],
  status: 200,       // HTTP 狀態碼
  statusText: 'OK',  // 狀態文本
  headers: {...},    // 回應頭
  config: {...}      // 請求配置
}

// 在模版中通常只需要 response.data
```

### 處理不同的狀態碼

```javascript
const fetchDogs = async () => {
  try {
    const response = await axios.get('/dogs/')
    // 200-299 都是成功
    console.log('取得成功:', response.data)
  } catch (error) {
    if (error.response) {
      // 伺服器回應了狀態碼，但是 4xx 或 5xx
      console.log('狀態碼:', error.response.status)
      console.log('錯誤訊息:', error.response.data)
      
      if (error.response.status === 404) {
        console.log('資源不存在')
      } else if (error.response.status === 400) {
        console.log('請求格式錯誤:', error.response.data.errors)
      }
    } else if (error.request) {
      // 發送了請求但沒有收到回應
      console.log('沒有收到回應')
    } else {
      // 請求設置出錯
      console.log('請求設置出錯:', error.message)
    }
  }
}
```

---

## 第五章：CORS 跨域與預檢請求

### 什麼是 CORS？

CORS (Cross-Origin Resource Sharing) 是解決跨域請求的標準。

**跨域的條件：**
```
協議 不同  http ≠ https
域名 不同  localhost ≠ example.com
端口 不同  3000 ≠ 8000
```

**前端請求：**
```
http://localhost:5173  →  http://127.0.0.1:8000
不同域名、不同端口 = 跨域
```

### Django 後端允許 CORS

```python
# settings.py 中配置

INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    # 必須放在最前面
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

# 允許的來源
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173',
]
```

### 預檢請求 (Preflight Request)

```
前端發送複雜請求
  ↓
瀏覽器先發送 OPTIONS 預檢請求
  ↓
後端回應是否允許跨域
  ↓
允許：發送實際請求
不允許：拋出 CORS 錯誤
```

**什麼是複雜請求：**
- PUT、DELETE、PATCH 方法
- 自訂 Header（如 `Content-Type: application/json`）
- 帶 Cookie 的請求

---

## 第六章：Loading 與 Error 狀態管理

### 基礎的加載狀態

```vue
<script setup>
import { ref } from 'vue'
import axios from 'axios'

const dogImage = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const fetchNewDog = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const response = await axios.get('https://dog.ceo/api/breeds/image/random')
    dogImage.value = response.data.message
  } catch (error) {
    errorMessage.value = '載入失敗，請重試'
    console.error('錯誤:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="dog-card">
    <p v-if="isLoading" class="loading">載入中...</p>
    <p v-else-if="errorMessage" class="error">{{ errorMessage }}</p>
    <img v-else :src="dogImage" alt="Random Dog" />
    
    <button @click="fetchNewDog" :disabled="isLoading">
      {{ isLoading ? '載入中...' : '換一張' }}
    </button>
  </div>
</template>
```

### 進階：使用 Composable 管理狀態

```javascript
// useAsyncData.js
import { ref } from 'vue'
import axios from 'axios'

export function useAsyncData(url) {
  const data = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  
  const fetchData = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await axios.get(url)
      data.value = response.data
    } catch (err) {
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }
  
  return { data, isLoading, error, fetchData }
}
```

**使用 Composable：**
```vue
<script setup>
import { onMounted } from 'vue'
import { useAsyncData } from './useAsyncData'

const { data: dogs, isLoading, error, fetchData } = useAsyncData('/dogs/')

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div>
    <p v-if="isLoading">載入中...</p>
    <p v-else-if="error">錯誤: {{ error }}</p>
    <ul v-else>
      <li v-for="dog in dogs" :key="dog.id">
        {{ dog.url }}
      </li>
    </ul>
  </div>
</template>
```

---

## 第七章：請求與回應攔截

### 請求攔截

```javascript
import axios from 'axios'

// 在發送每個請求前執行
axios.interceptors.request.use(
  config => {
    // 添加認證令牌
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 添加自訂 Header
    config.headers['X-Custom-Header'] = 'my-value'
    
    console.log('發送請求:', config.url)
    return config
  },
  error => {
    return Promise.reject(error)
  }
)
```

### 回應攔截

```javascript
axios.interceptors.response.use(
  response => {
    // 成功回應
    console.log('收到回應:', response.status)
    return response
  },
  error => {
    // 錯誤回應
    if (error.response?.status === 401) {
      // 認證失敗，跳轉登入
      window.location.href = '/login'
    } else if (error.response?.status === 403) {
      // 無權限
      console.error('無權限')
    }
    
    return Promise.reject(error)
  }
)
```

---

## 總結

前後端交互要點：
✅ 使用 Axios 簡化 HTTP 請求
✅ 掌握 async/await 非同步操作
✅ 理解 CORS 跨域問題
✅ 正確處理加載和錯誤狀態
✅ 利用攔截器統一管理請求
✅ 構建可複用的資料獲取邏輯
