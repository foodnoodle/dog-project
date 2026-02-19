import api from '../utils/api';

export const chatApi = {
    /**
     * 獲取特定圖片的歷史對話紀錄
     * @param {string} imageUrl - 狗狗圖片網址
     */
    getHistory(imageUrl) {
        return api.get('/api/chat/ask/', {
            params: { image_url: imageUrl }
        });
    },

    /**
     * 針對狗狗圖片發送新問題
     * @param {string} imageUrl - 狗狗圖片網址
     * @param {string} prompt - 使用者的提問
     */
    askQuestion(imageUrl, prompt) {
        return api.post('/api/chat/ask/', {
            image_url: imageUrl,
            prompt: prompt
        });
    },

    /**
     * 清空特定圖片的對話紀錄
     * @param {string} imageUrl - 狗狗圖片網址
     */
    clearHistory(imageUrl) {
        return api.delete('/api/chat/ask/', {
            data: { image_url: imageUrl }
        });
    },

    /**
     * 獲取所有對話紀錄列表
     */
    getAllSessions() {
        return api.get('/api/chat/ask/');
    },

    /**
     * 清除所有對話紀錄
     */
    deleteAllSessions() {
        return api.delete('/api/chat/ask/');
    }
};
