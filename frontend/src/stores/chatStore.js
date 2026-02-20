import { defineStore } from 'pinia';
import { chatApi } from '../api/chat';

export const useChatStore = defineStore('chat', {
    state: () => ({
        isOpen: false,          // 控制右側抽屜是否展開
        currentImageUrl: '',    // 目前正在對話的狗狗圖片網址
        messages: [],           // 當前的對話紀錄陣列
        isLoading: false,       // 控制 AI 思考時的載入狀態
        error: null,            // 錯誤訊息狀態
    }),

    actions: {
        /**
         * 打開抽屜並載入歷史紀錄
         * @param {string} imageUrl - 狗狗圖片網址
         */
        async openDrawer(imageUrl) {
            this.isOpen = true;
            this.currentImageUrl = imageUrl;
            await this.fetchHistory(imageUrl);
        },

        /**
         * 關閉抽屜並重置狀態
         */
        closeDrawer() {
            this.isOpen = false;
            this.currentImageUrl = '';
            this.messages = [];
            this.error = null;
        },

        /**
         * 獲取歷史紀錄
         */
        async fetchHistory(imageUrl) {
            this.isLoading = true;
            this.error = null;
            try {
                const response = await chatApi.getHistory(imageUrl);
                // 後端序列化器回傳的資料中包含 messages 陣列
                this.messages = (response.data.messages || []).map(msg => ({
                    ...msg,
                    isNew: false // History messages are not new
                }));
            } catch (err) {
                if (err.response && err.response.data && err.response.data.error) {
                    this.error = err.response.data.error;
                } else {
                    this.error = '無法載入歷史對話';
                }
                console.error('Fetch history error:', err);
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 發送訊息給 AI
         * @param {string} prompt - 使用者輸入的問題
         */
        async sendMessage(prompt) {
            if (!prompt.trim() || !this.currentImageUrl) return;

            // 1. 樂觀 UI 更新 (Optimistic UI)：先將使用者的問題顯示在畫面上
            this.messages.push({ role: 'user', content: prompt, isNew: false });
            this.isLoading = true;
            this.error = null;

            try {
                // 2. 發送 API 請求
                const response = await chatApi.askQuestion(this.currentImageUrl, prompt);

                // 3. 將 AI 的回覆加入對話陣列中，標記為新訊息以觸發打字機效果
                this.messages.push({ role: 'model', content: response.data.response, isNew: true });
            } catch (err) {
                if (err.response && err.response.data && err.response.data.error) {
                    this.error = err.response.data.error;
                } else {
                    this.error = 'AI 回覆失敗，請稍後再試';
                }
                console.error('Send message error:', err);
                // 專業做法：若發送失敗，可以選擇在此移除剛才樂觀更新的訊息，或加上錯誤標記
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 清空當前圖片的歷史紀錄
         */
        async clearCurrentHistory() {
            if (!this.currentImageUrl) return;
            this.isLoading = true;
            try {
                await chatApi.clearHistory(this.currentImageUrl);
                this.messages = []; // 清空前端畫面
            } catch (err) {
                if (err.response && err.response.data && err.response.data.error) {
                    this.error = err.response.data.error;
                } else {
                    this.error = '清空歷史紀錄失敗';
                }
                console.error('Clear history error:', err);
            } finally {
                this.isLoading = false;
            }
        }
    }
});