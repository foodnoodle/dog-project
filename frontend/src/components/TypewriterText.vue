<template>
    <span class="whitespace-pre-wrap">{{ displayedText }}<span v-if="isTyping" class="animate-pulse">|</span></span>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
    text: {
        type: String,
        required: true
    },
    speed: {
        type: Number,
        default: 30 // milliseconds per character
    }
});

const emit = defineEmits(['update', 'complete']);

const displayedText = ref('');
const isTyping = ref(true);
let currentIndex = 0;
let timeoutId = null;

const typeText = () => {
    if (currentIndex < props.text.length) {
        // Handling potential markdown or HTML could be tricky here, 
        // but for simple text, character by character is fine.
        // If the text has Markdown, we might need a more complex approach,
        // but a fast enough speed usually makes it look okay even with markdown.
        displayedText.value += props.text.charAt(currentIndex);
        currentIndex++;
        emit('update');

        // Add brief varying delay for more realistic typing
        const variation = Math.random() * 20 - 10;
        const currentSpeed = Math.max(10, props.speed + variation);

        timeoutId = setTimeout(typeText, currentSpeed);
    } else {
        isTyping.value = false;
        emit('complete');
    }
};

onMounted(() => {
    typeText();
});

onUnmounted(() => {
    if (timeoutId) {
        clearTimeout(timeoutId);
    }
});

// Watch for changes if text updates (shouldn't happen often in this use case, but good practice)
watch(() => props.text, (newText) => {
    // If text was fully typed, and now it changed (e.g., getting longer)
    if (currentIndex < newText.length) {
        if (!isTyping.value) {
            isTyping.value = true;
            typeText();
        }
    }
});
</script>

<style scoped>
/* Optional: slightly soften the cursor pulse if needed */
.animate-pulse {
    animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0;
    }
}
</style>
