// frontend/src/utils/api.js
import axios from 'axios';

/**
 * 建立 Axios 實體 (Instance)
 * 說明：
 * 透過 create 方法建立一個獨立的 axios 物件，
 * 這樣可以避免汙染全域的 axios 設定，並統一管理基礎路徑與超時設定。
 */
const api = axios.create({
  // 1. 基礎路徑：自動讀取 .env 檔案中的 VITE_API_BASE_URL 變數
  // 如果忘記設定 .env，這裡給一個空字串作為備用，避免程式直接崩潰
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  
  // 2. 超時設定：請求超過 10 秒無回應則自動中斷 (單位：毫秒)
  timeout: 10000,
  
  // 3. 預設標頭：告訴後端我們傳送的是 JSON 格式資料
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 響應攔截器 (Response Interceptor)
 * 說明：
 * 在「瀏覽器收到後端回應」之後，「程式碼 (.vue) 拿到資料」之前執行。
 * 用途：統一處理成功回應或全域錯誤 (如網路斷線、401 未授權等)。
 */
api.interceptors.response.use(
  // A. 請求成功 (Status Code 2xx)
  (response) => {
    // 直接回傳後端的回應物件
    return response;
  },
  
  // B. 請求失敗 (Status Code 非 2xx 或網路錯誤)
  (error) => {
    console.error('【API 異常】:', error);

    // 針對常見錯誤進行統一處理，省去在每個頁面重複寫 try-catch 的 alert
    if (error.code === 'ERR_NETWORK') {
      alert('無法連線至伺服器，請檢查後端 (Django) 是否已啟動。');
    } else if (error.response && error.response.status === 500) {
      alert('伺服器發生內部錯誤，請聯絡管理員。');
    }
    
    // 將錯誤繼續往下拋，讓個別組件仍有機會處理特定邏輯 (例如按鈕恢復可點擊狀態)
    return Promise.reject(error);
  }
);

// 匯出這個設定好的實體，供其他組件使用
export default api;