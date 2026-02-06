import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // 1. 引入我們剛建立的路由設定

const app = createApp(App)

app.use(router) // 2. 告訴 Vue 啟用路由功能
app.mount('#app')