<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <div class="top-nav" v-if="user">
      <div class="nav-left">
        <h1 class="app-title">🤖 AI代码生成平台</h1>
      </div>
      <div class="nav-right">
        <span class="user-name">{{ user.email }}</span>
        <button @click="handleLogout" class="logout-btn">退出</button>
      </div>
    </div>

    <!-- 未登录状态 -->
    <div v-if="!user && !loading" class="login-container">
      <div class="login-card">
        <h1>🚀 欢迎使用 AI代码生成平台</h1>
        <p>基于 Atoms Cloud 和 AI 技术</p>
        <button @click="handleLogin" class="login-btn">
          登录以开始使用
        </button>
      </div>
    </div>

    <!-- 已登录状态 -->
    <div v-else-if="user" class="main-content">
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

    <!-- 加载状态 -->
    <div v-else class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ChatPanel from './components/ChatPanel.vue';
import PreviewPanel from './components/PreviewPanel.vue';
import CodeEditor from './components/CodeEditor.vue';
import { generateCode } from './services/api';
import { auth } from './services/atomsCloud';
import type { Message, GeneratedCode } from './types';

const user = ref<any>(null);
const loading = ref(true);
const messages = ref<Message[]>([]);
const generatedCode = ref<GeneratedCode | null>(null);
const isGenerating = ref(false);
const showCodeEditor = ref(false);

onMounted(async () => {
  try {
    const currentUser = await auth.getCurrentUser();
    user.value = currentUser;
  } catch (error) {
    console.error('获取用户信息失败:', error);
  } finally {
    loading.value = false;
  }
});

const handleLogin = async () => {
  await auth.toLogin();
};

const handleLogout = async () => {
  await auth.logout();
  user.value = null;
  messages.value = [];
  generatedCode.value = null;
};

const handleSendMessage = async (content: string) => {
  const userMessage: Message = {
    id: Date.now().toString(),
    role: 'user',
    content,
    timestamp: Date.now()
  };
  messages.value.push(userMessage);

  isGenerating.value = true;

  try {
    const processingMessage: Message = {
      id: `${Date.now()}-processing`,
      role: 'assistant',
      content: '🤖 正在使用 Atoms AI 生成代码...',
      timestamp: Date.now()
    };
    messages.value.push(processingMessage);

    const response = await generateCode(content);
    
    if (response.code) {
      generatedCode.value = response.code;
      
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
  flex-direction: column;
  height: 100vh;
  background: #0A0A0A;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #1A1A1A;
  border-bottom: 1px solid #2A2A2A;
}

.nav-left {
  display: flex;
  align-items: center;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  color: #9CA3AF;
  font-size: 0.875rem;
}

.logout-btn {
  background: #6366F1;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #5558E3;
}

.login-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 3rem;
  border-radius: 24px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  text-align: center;
  max-width: 400px;
}

.login-card h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
}

.login-card p {
  color: #666;
  margin-bottom: 2rem;
}

.login-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: transform 0.2s;
}

.login-btn:hover {
  transform: translateY(-2px);
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>