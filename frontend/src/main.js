import { createApp } from 'vue'
import { createPinia } from 'pinia' // 引入 Pinia
import './style.css'
import App from './App.vue'
import router from './router' // 引入我們剛建立的路由設定

const app = createApp(App)

app.use(createPinia()) // 告訴 Vue 啟用 Pinia 功能
app.use(router) // 告訴 Vue 啟用路由功能
app.mount('#app')