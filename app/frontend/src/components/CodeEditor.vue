<template>
  <div class="code-editor-overlay" @click.self="$emit('close')">
    <div class="code-editor-modal">
      <!-- Header -->
      <div class="modal-header">
        <h2 class="modal-title">生成的代码</h2>
        <div class="header-actions">
          <button @click="downloadCode" class="action-btn">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            下载
          </button>
          <button @click="$emit('close')" class="action-btn">关闭</button>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs-container">
        <div class="tabs-list">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            @click="activeTab = tab.value"
            class="tab-button"
            :class="{ active: activeTab === tab.value }"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- Code Content -->
      <div class="code-content">
        <button @click="copyCode(activeTab)" class="copy-button">
          <svg v-if="copiedTab !== activeTab" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="20 6 9 17 4 12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ copiedTab === activeTab ? '已复制' : '复制' }}
        </button>
        <div class="code-scroll">
          <pre class="code-block"><code>{{ currentCode }}</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { GeneratedCode } from '../types';

interface Props {
  code: GeneratedCode;
}

const props = defineProps<Props>();
defineEmits<{
  (e: 'close'): void;
}>();

const tabs = [
  { label: 'HTML', value: 'html' },
  { label: 'CSS', value: 'css' },
  { label: 'JavaScript', value: 'javascript' }
];

const activeTab = ref<'html' | 'css' | 'javascript'>('html');
const copiedTab = ref<string | null>(null);

const currentCode = computed(() => {
  return props.code[activeTab.value] || '';
});

const copyCode = (tab: string) => {
  const code = props.code[tab as keyof GeneratedCode];
  navigator.clipboard.writeText(code);
  copiedTab.value = tab;
  setTimeout(() => {
    copiedTab.value = null;
  }, 2000);
};

const downloadCode = () => {
  const content = `
HTML文件:
${props.code.html}

---

CSS文件:
${props.code.css}

---

JavaScript文件:
${props.code.javascript}
  `;

  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'generated-code.txt';
  a.click();
  URL.revokeObjectURL(url);
};
</script>

<style scoped>
.code-editor-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.code-editor-modal {
  background: #0A0A0A;
  border: 1px solid #2A2A2A;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 56rem;
  height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #2A2A2A;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
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

.action-btn:hover {
  background: #2A2A2A;
  color: white;
}

.btn-icon {
  width: 1rem;
  height: 1rem;
}

.tabs-container {
  background: #1A1A1A;
  border-bottom: 1px solid #2A2A2A;
}

.tabs-list {
  display: flex;
  padding: 0.5rem;
  gap: 0.25rem;
}

.tab-button {
  background: transparent;
  border: none;
  color: #9CA3AF;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.tab-button:hover {
  background: #2A2A2A;
}

.tab-button.active {
  background: #6366F1;
  color: white;
}

.code-content {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.copy-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
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

.copy-button:hover {
  background: #2A2A2A;
  color: white;
}

.code-scroll {
  height: 100%;
  overflow: auto;
}

.code-block {
  padding: 1.5rem;
  font-size: 0.875rem;
  font-family: 'Fira Code', 'Courier New', monospace;
  color: #E5E7EB;
  background: #0A0A0A;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>