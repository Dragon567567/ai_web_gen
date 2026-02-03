<template>
  <div class="app-container">
    <ChatPanel
      :messages="messages"
      :is-generating="isGenerating"
      @send-message="handleSendMessage"
    />
    <PreviewPanel
      :code="generatedCode"
      @show-code="showCodeEditor = true"
    />
    <CodeEditor
      v-if="showCodeEditor && generatedCode"
      :code="generatedCode"
      @close="showCodeEditor = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ChatPanel from './components/ChatPanel.vue';
import PreviewPanel from './components/PreviewPanel.vue';
import CodeEditor from './components/CodeEditor.vue';
import { generateCode } from './services/api';
import type { Message, GeneratedCode } from './types';

const messages = ref<Message[]>([]);
const generatedCode = ref<GeneratedCode | null>(null);
const isGenerating = ref(false);
const showCodeEditor = ref(false);

const handleSendMessage = async (content: string) => {
  // 添加用户消息
  const userMessage: Message = {
    id: Date.now().toString(),
    role: 'user',
    content,
    timestamp: Date.now()
  };
  messages.value.push(userMessage);

  isGenerating.value = true;

  try {
    // 添加AI处理消息
    const processingMessage: Message = {
      id: `${Date.now()}-processing`,
      role: 'assistant',
      content: '正在分析您的需求并生成代码...',
      timestamp: Date.now()
    };
    messages.value.push(processingMessage);

    // 调用API生成代码
    const response = await generateCode(content);
    
    if (response.code) {
      generatedCode.value = response.code;
      
      // 更新消息为成功
      const successMessage: Message = {
        id: `${Date.now()}-success`,
        role: 'assistant',
        content: '✅ 代码生成完成！您可以在右侧预览效果，或点击"查看代码"按钮查看源代码。',
        timestamp: Date.now()
      };
      messages.value = messages.value.filter(m => m.id !== processingMessage.id);
      messages.value.push(successMessage);
    } else {
      throw new Error(response.message);
    }
  } catch (error) {
    const errorMessage: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content: `❌ 生成失败: ${error instanceof Error ? error.message : '未知错误'}`,
      timestamp: Date.now()
    };
    messages.value = messages.value.filter(m => !m.id.includes('processing'));
    messages.value.push(errorMessage);
  } finally {
    isGenerating.value = false;
  }
};
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  background: #0A0A0A;
}
</style>