// frontend/src/stores/auth.js
import { defineStore } from 'pinia';
import api from '../utils/api'; // 引入我們剛剛寫好的那個 api 工具

export const useAuthStore = defineStore('auth', {
    // 1. 狀態 (State): 就像是倉庫，存變數的地方
    state: () => ({
        // 初始化時，先去 localStorage 找找看有沒有舊的 token
        token: localStorage.getItem('token') || null,
        // 雖然目前後端只回傳 key，但預留 user 欄位未來可以用
        user: JSON.parse(localStorage.getItem('user')) || null,
    }),

    // 2. 計算屬性 (Getters): 就像是倉庫的查詢員
    getters: {
        // 只要 token 不是空的，就代表「已登入」
        isAuthenticated: (state) => !!state.token,
    },

    // 3. 動作 (Actions): 就像是倉庫的管理員，負責改資料
    actions: {
        // === 登入功能 ===
        async login(username, password) {
            try {
                // 向後端發送登入請求 (注意：不用寫 http://localhost...，因為 api.js 裡設定好了)
                const response = await api.post('/api/auth/login/', {
                    username,
                    password,
                });

                // 拿到後端發給我們的通行證 (Key)
                const token = response.data.key;

                // 存到 Pinia 狀態中 (讓畫面可以馬上反應)
                this.token = token;

                // 存到瀏覽器硬碟中 (讓重新整理後還記得)
                localStorage.setItem('token', token);

                // (選用) 如果後端有回傳 user 資訊，也可以存起來
                // this.user = response.data.user;

                return true; // 告訴呼叫者：登入成功！
            } catch (error) {
                console.error('登入失敗:', error);
                throw error; // 把錯誤往外丟，讓 Login 頁面去顯示紅字錯誤
            }
        },

        // === 註冊功能 ===
        async register(username, password, passwordConfirm) {
            try {
                // 呼叫後端註冊 API
                // dj-rest-auth 的標準註冊路徑是 /registration/
                await api.post('/api/auth/registration/', {
                    username,
                    password1: password,       // ✅ 這是主密碼
                    password2: passwordConfirm // ✅ 這是確認密碼
                });

                // 註冊成功後，通常後端會直接回傳 Token (視設定而定)
                // 但為了保險起見，我們讓使用者註冊完後，自動執行一次「登入」
                return await this.login(username, password);

            } catch (error) {
                console.error('註冊失敗:', error);
                throw error;
            }
        },

        // === 登出功能 ===
        logout() {
            // 1. 清空狀態
            this.token = null;
            this.user = null;

            // 2. 清除瀏覽器紀錄
            localStorage.removeItem('token');
            localStorage.removeItem('user');

            // (選用) 如果想要更嚴謹，可以發送請求通知後端銷毀 Token
            // await api.post('/auth/logout/');
        },
    },
});