<template>
  <div class="preview-panel">
    <!-- Header -->
    <div class="preview-header">
      <div class="header-left">
        <img 
          src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/7ae694b7-0026-4c24-a5b1-f819287f07ab.png" 
          alt="Preview" 
          class="header-icon"
        />
        <h2 class="header-title">实时预览</h2>
      </div>
      <div class="header-actions">
        <button @click="$emit('show-code')" class="action-btn">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M16 18l6-6-6-6M8 6l-6 6 6 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          查看代码
        </button>
        <button @click="handleRefresh" :disabled="isRefreshing" class="action-btn">
          <svg class="btn-icon" :class="{ 'spinning': isRefreshing }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M1 4v6h6M23 20v-6h-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <button @click="handleFullscreen" class="action-btn">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Preview -->
    <div class="preview-content">
      <div v-if="!code" class="empty-preview">
        <div class="empty-icon-wrapper">
          <img 
            src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/a1e8ad55-b48b-4171-bc62-1e420e88a3fc.png" 
            alt="Code" 
            class="empty-icon"
          />
        </div>
        <p class="empty-title">等待AI生成代码...</p>
        <p class="empty-subtitle">在左侧输入你的需求开始</p>
      </div>
      <iframe
        v-else
        ref="iframeRef"
        class="preview-iframe"
        title="预览"
        sandbox="allow-scripts allow-same-origin"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import type { GeneratedCode } from '../types';

interface Props {
  code: GeneratedCode | null;
}

const props = defineProps<Props>();
defineEmits<{
  (e: 'show-code'): void;
}>();

const iframeRef = ref<HTMLIFrameElement | null>(null);
const isRefreshing = ref(false);

const updatePreview = () => {
  if (!props.code || !iframeRef.value) return;

  const iframe = iframeRef.value;
  const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;

  if (iframeDoc) {
    const fullHTML = `
      <!DOCTYPE html>
      <html lang="zh-CN">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>${props.code.css}</style>
      </head>
      <body>
        ${props.code.html.replace(/<link[^>]*>/g, '').replace(/<script[^>]*src[^>]*><\/script>/g, '')}
        <script>${props.code.javascript}</script>
      </body>
      </html>
    `;

    iframeDoc.open();
    iframeDoc.write(fullHTML);
    iframeDoc.close();
  }
};

const handleRefresh = () => {
  isRefreshing.value = true;
  updatePreview();
  setTimeout(() => {
    isRefreshing.value = false;
  }, 500);
};

const handleFullscreen = () => {
  if (iframeRef.value) {
    iframeRef.value.requestFullscreen();
  }
};

watch(() => props.code, () => {
  nextTick(() => {
    updatePreview();
  });
}, { deep: true });
</script>

<style scoped>
.preview-panel {
  flex: 1;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0A0A0A;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #2A2A2A;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.header-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: #1A1A1A;
  border: 1px solid #2A2A2A;
  color: #9CA3AF;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.action-btn:hover:not(:disabled) {
  background: #2A2A2A;
  color: white;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  width: 1rem;
  height: 1rem;
}

.spinning {
  animation: spin 0.8s linear infinite;
}

.preview-content {
  flex: 1;
  position: relative;
  background: white;
}

.empty-preview {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #0A0A0A;
}

.empty-icon-wrapper {
  width: 6rem;
  height: 6rem;
  background: #1A1A1A;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.empty-icon {
  width: 3rem;
  height: 3rem;
}

.empty-title {
  color: #9CA3AF;
  font-size: 1.125rem;
  margin: 0 0 0.5rem 0;
}

.empty-subtitle {
  color: #6B7280;
  font-size: 0.875rem;
  margin: 0;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>