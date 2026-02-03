<template>
  <div class="chat-panel">
    <!-- Header -->
    <div class="chat-header">
      <div class="header-content">
        <img 
          src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/156803cf-57c8-4490-bd72-b524372384f1.png" 
          alt="Chat" 
          class="header-icon"
        />
        <div>
          <h2 class="header-title">AI代码助手</h2>
          <p class="header-subtitle">描述你想要的应用</p>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div class="messages-container" ref="messagesRef">
      <div v-if="messages.length === 0" class="empty-state">
        <img 
          src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/fd29a045-7a51-4fd6-819d-35cfe69b3241.png" 
          alt="AI Coding" 
          class="empty-image"
        />
        <p class="empty-text">开始对话，让AI为你生成代码</p>
        <div class="examples">
          <p class="examples-title">试试这些示例：</p>
          <div class="examples-buttons">
            <button @click="$emit('send-message', '创建一个计数器应用')" class="example-btn">
              计数器应用
            </button>
            <button @click="$emit('send-message', '创建一个待办事项列表')" class="example-btn">
              待办列表
            </button>
            <button @click="$emit('send-message', '创建一个简单的个人主页')" class="example-btn">
              个人主页
            </button>
          </div>
        </div>
      </div>

      <div v-for="message in messages" :key="message.id" class="message-wrapper" :class="message.role">
        <div class="message-bubble" :class="message.role">
          <p class="message-content">{{ message.content }}</p>
          <p class="message-time">{{ formatTime(message.timestamp) }}</p>
        </div>
      </div>

      <div v-if="isGenerating" class="message-wrapper assistant">
        <div class="message-bubble assistant">
          <div class="generating">
            <div class="spinner"></div>
            <span>AI正在生成代码...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="input-container">
      <textarea
        v-model="inputValue"
        @keydown.enter.prevent="handleSend"
        placeholder="描述你想要创建的应用..."
        class="input-textarea"
        :disabled="isGenerating"
      />
      <button
        @click="handleSend"
        :disabled="!inputValue.trim() || isGenerating"
        class="send-button"
      >
        <svg v-if="!isGenerating" class="send-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div v-else class="spinner"></div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue';
import type { Message } from '../types';

interface Props {
  messages: Message[];
  isGenerating: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'send-message', content: string): void;
}>();

const inputValue = ref('');
const messagesRef = ref<HTMLElement | null>(null);

const handleSend = () => {
  if (inputValue.value.trim() && !props.isGenerating) {
    emit('send-message', inputValue.value.trim());
    inputValue.value = '';
  }
};

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

watch(() => props.messages.length, () => {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
    }
  });
});
</script>

<style scoped>
.chat-panel {
  width: 40%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0A0A0A;
  border-right: 1px solid #2A2A2A;
}

.chat-header {
  padding: 1.5rem;
  border-bottom: 1px solid #2A2A2A;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  width: 2rem;
  height: 2rem;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.header-subtitle {
  font-size: 0.875rem;
  color: #9CA3AF;
  margin: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
}

.empty-image {
  width: 100%;
  max-width: 28rem;
  margin: 0 auto 1.5rem;
  border-radius: 0.5rem;
  opacity: 0.8;
}

.empty-text {
  color: #9CA3AF;
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.examples {
  margin-top: 1.5rem;
}

.examples-title {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 0.5rem;
}

.examples-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.example-btn {
  background: #1A1A1A;
  border: 1px solid #2A2A2A;
  color: #9CA3AF;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.example-btn:hover {
  background: #2A2A2A;
  color: white;
}

.message-wrapper {
  display: flex;
  margin-bottom: 1rem;
}

.message-wrapper.user {
  justify-content: flex-end;
}

.message-wrapper.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 80%;
  padding: 1rem;
  border-radius: 0.5rem;
}

.message-bubble.user {
  background: #6366F1;
  color: white;
}

.message-bubble.assistant {
  background: #1A1A1A;
  color: #E5E7EB;
  border: 1px solid #2A2A2A;
}

.message-content {
  white-space: pre-wrap;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0 0 0.5rem 0;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.6;
  margin: 0;
}

.generating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.input-container {
  padding: 1.5rem;
  border-top: 1px solid #2A2A2A;
  display: flex;
  gap: 0.5rem;
}

.input-textarea {
  flex: 1;
  min-height: 60px;
  max-height: 120px;
  background: #1A1A1A;
  border: 1px solid #2A2A2A;
  color: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  resize: none;
  font-family: inherit;
  font-size: 0.875rem;
}

.input-textarea::placeholder {
  color: #6B7280;
}

.input-textarea:focus {
  outline: none;
  border-color: #6366F1;
}

.input-textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-button {
  background: #6366F1;
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  background: #5558E3;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>