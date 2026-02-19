<template>
    <transition name="fade">
        <div v-if="chatStore.isOpen" class="fixed inset-0 bg-black bg-opacity-40 z-40 backdrop-blur-sm"
            @click="chatStore.closeDrawer">
        </div>
    </transition>

    <transition name="slide">
        <div v-if="chatStore.isOpen"
            class="fixed inset-y-0 right-0 w-full md:w-[420px] bg-white shadow-2xl z-50 flex flex-col">

            <header class="p-4 border-b flex items-center justify-between bg-white">
                <div class="flex items-center gap-3">
                    <img :src="chatStore.currentImageUrl" alt="Dog Thumbnail"
                        class="w-12 h-12 rounded-lg object-cover shadow-sm border" />
                    <h2 class="text-lg font-bold text-gray-800 tracking-wide">AI 狗狗助理</h2>
                </div>
                <div class="flex items-center gap-1">
                    <button @click="chatStore.clearCurrentHistory"
                        class="p-2 text-gray-400 hover:text-red-500 transition-colors rounded-full hover:bg-red-50"
                        title="清空對話">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                    <button @click="chatStore.closeDrawer"
                        class="p-2 text-gray-400 hover:text-gray-700 transition-colors rounded-full hover:bg-gray-100"
                        title="關閉">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </header>

            <main class="flex-1 overflow-y-auto p-4 space-y-5 bg-gray-50 scroll-smooth" ref="chatContainer">
                <div v-if="chatStore.messages.length === 0 && !chatStore.isLoading"
                    class="text-center text-gray-400 mt-10 text-sm">
                    <p>這隻狗狗好可愛！✨<br>想知道牠是什麼品種，或是毛髮怎麼整理嗎？</p>
                </div>

                <div v-for="(msg, index) in chatStore.messages" :key="index" class="flex flex-col"
                    :class="msg.role === 'user' ? 'items-end' : 'items-start'">
                    <span class="text-xs text-gray-400 mb-1 px-1">{{ msg.role === 'user' ? '您' : 'AI 助理' }}</span>
                    <div class="max-w-[85%] rounded-2xl px-4 py-2.5 shadow-sm" :class="msg.role === 'user'
                        ? 'bg-blue-600 text-white rounded-tr-none'
                        : 'bg-white text-gray-700 border border-gray-100 rounded-tl-none'">
                        <p class="whitespace-pre-wrap text-sm leading-relaxed">{{ msg.content }}</p>
                    </div>
                </div>

                <div v-if="chatStore.isLoading" class="flex flex-col items-start">
                    <span class="text-xs text-gray-400 mb-1 px-1">AI 助理思考中...</span>
                    <div
                        class="bg-white border border-gray-100 rounded-2xl rounded-tl-none px-4 py-3.5 shadow-sm flex items-center gap-1.5">
                        <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
                        <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"
                            style="animation-delay: 0.15s"></span>
                        <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"
                            style="animation-delay: 0.3s"></span>
                    </div>
                </div>
            </main>

            <footer class="p-4 border-t bg-white">
                <div v-if="chatStore.error" class="text-red-500 text-xs mb-2 text-center">
                    {{ chatStore.error }}
                </div>
                <form @submit.prevent="handleSend" class="flex gap-2 relative">
                    <input v-model="prompt" type="text" placeholder="輸入您的問題..."
                        class="flex-1 border border-gray-300 rounded-full pl-5 pr-12 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm transition-shadow shadow-sm"
                        :disabled="chatStore.isLoading" />
                    <button type="submit"
                        class="absolute right-1.5 top-1.5 bottom-1.5 aspect-square bg-blue-600 text-white rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors disabled:bg-gray-300 shadow-sm"
                        :disabled="!prompt.trim() || chatStore.isLoading">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor" stroke-width="2.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 19V5m0 0l-7 7m7-7l7 7" />
                        </svg>
                    </button>
                </form>
            </footer>

        </div>
    </transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { useChatStore } from '../stores/chatStore'; // 請確保路徑正確

const chatStore = useChatStore();
const prompt = ref('');
const chatContainer = ref(null);

/**
 * 處理訊息發送
 */
const handleSend = async () => {
    if (!prompt.value.trim() || chatStore.isLoading) return;
    const question = prompt.value;
    prompt.value = ''; // 提早清空輸入框，讓使用者感覺系統反應極快
    await chatStore.sendMessage(question);
};

/**
 * 核心講究細節：自動捲動到底部
 * 當 messages 陣列長度改變時，自動將對話框捲動到最新的一筆訊息
 */
watch(() => chatStore.messages.length, async () => {
    await nextTick(); // 等待 Vue 完成 DOM 渲染
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
});
</script>

<style scoped>
/* 定義 Vue 的平滑轉場動畫 */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

/* 抽屜從右側滑出的動畫 */
.slide-enter-active,
.slide-leave-active {
    transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.slide-enter-from,
.slide-leave-to {
    transform: translateX(100%);
}
</style>