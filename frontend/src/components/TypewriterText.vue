<template>
    <div class="markdown-container" v-html="parsedHTML"></div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

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

const parsedHTML = computed(() => {
    let html = DOMPurify.sanitize(marked.parse(displayedText.value));

    // In order to show the cursor inline with the last paragraph, we inject it into the HTML natively.
    if (isTyping.value) {
        if (html.endsWith('</p>\n')) {
            html = html.slice(0, -5) + '<span class="typing-cursor">|</span></p>\n';
        } else {
            html += '<span class="typing-cursor">|</span>';
        }
    }
    return html;
});

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
:deep(p) {
    margin-bottom: 0.5rem;
}

:deep(p:last-child) {
    margin-bottom: 0;
}

:deep(strong) {
    font-weight: 700;
}

:deep(ul) {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 0.5rem;
}

:deep(li) {
    margin-bottom: 0.25rem;
}

:deep(.typing-cursor) {
    display: inline-block;
    animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    margin-left: 2px;
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
